# -*- coding: utf-8 -*-
from odoo import models
import logging

_logger = logging.getLogger(__name__)

# ── Formula fixes for top-level lines ──────────────────────────────────────
# {line_code: (formula, subformula)}
#
# Goal: Match Partner Ledger balance column exactly (DYNAMIC - no hardcoded account codes)
#
#   Partner Ledger Balance = debit - credit per partner
#   Receivable partners  → POSITIVE (+) (customer owes us)
#   Payable partners     → NEGATIVE (-) (we owe vendor)
#
#   Odoo domain engine:
#     'sum'  = debit - credit
#     '-sum' = credit - debit
#
#   For asset_receivable: debit > credit → 'sum' = POSITIVE (+)
#   For liability_payable: credit > debit → 'sum' = NEGATIVE (-)
FORMULA_FIXES = {
    # BANK AND CASH BALANCE → Match Balance Sheet: sum([('account_id.account_type', '=', 'asset_cash')])
    'bank_cash_bal': (
        "[('account_id.account_type', '=', 'asset_cash')]",
        'sum'
    ),

    # ACCOUNT RECEIVABLES → Plus (+) values
    'acc_rec': (
        "[('account_id.account_type', '=', 'asset_receivable'), ('account_id.non_trade', '=', False)]",
        '-sum'
    ),

    # ACCOUNT PAYABLES → Minus (-) values
    'acc_pay': (
        "[('account_id.account_type', '=', 'liability_payable'), ('account_id.non_trade', '=', False)]",
        '-sum'
    ),
}

# ── Child lines to create under 'Total Receivable/Payable' ─────────────────
CHILD_LINES = [
    {
        'name': 'Total Receivables',
        'code': 'tot_rec_sub',
        'sequence_offset': 1,
        'foldable': False,
        'hide_if_zero': False,
        'formula': "[('account_id.account_type', '=', 'asset_receivable'), ('account_id.non_trade', '=', False)]",
        'subformula': '-sum',      # '-sum' → POSITIVE (+) values
    },
    {
        'name': 'Total Payables',
        'code': 'tot_pay_sub',
        'sequence_offset': 2,
        'foldable': False,
        'hide_if_zero': False,
        'formula': "[('account_id.account_type', '=', 'liability_payable'), ('account_id.non_trade', '=', False)]",
        'subformula': '-sum',      # '-sum' → NEGATIVE (-) values
    },
]


class ImanAccountSummaryFix(models.AbstractModel):
    """
    Runs on every module install/upgrade to fix Account Summary report:

    1. FORMULA FIX (Dynamic - Partner Ledger approach):
       - ACCOUNT RECEIVABLES (acc_rec): asset_receivable, non_trade=False
         subformula='sum' → POSITIVE (+) values matching Partner Ledger customer balances
       - ACCOUNT PAYABLES (acc_pay): liability_payable, non_trade=False
         subformula='sum' → NEGATIVE (-) values matching Partner Ledger vendor balances

    2. REVERT: Restore acc_rec and acc_pay to top-level (no parent_id)

    3. TOTAL Receivable/Payable PARENT & CHILDREN:
       - Create / ensure 'Total Receivable/Payable' parent line with code 'tot_rec_pay_parent'
       - Make it foldable with aggregated NET value (tot_rec_sub.balance + tot_pay_sub.balance)
         displayed right in front of 'Total Receivable/Payable'
       - Add 'Total Receivables' child → POSITIVE (+) asset_receivable
       - Add 'Total Payables' child   → NEGATIVE (-) liability_payable
    """
    _name = 'iman.account.summary.fix'
    _description = 'Iman Account Summary Formula Fix'

    def _register_hook(self):
        super()._register_hook()
        # Clean up any bad subformula 'if_other_false' in existing database expressions
        try:
            with self.env.cr.savepoint():
                bad_exprs = self.env['account.report.expression'].search([('subformula', '=', 'if_other_false')])
                if bad_exprs:
                    bad_exprs.sudo().write({'subformula': False})
                    _logger.info('iman_account_summary: Cleared invalid subformula "if_other_false" from %s expressions.', len(bad_exprs))
        except Exception as e:
            _logger.error('iman_account_summary: Error cleaning up if_other_false expressions: %s', e)

        # Each method is wrapped in its own savepoint so that if one fails,
        # the PostgreSQL transaction is NOT left in an aborted state.
        for method in [
            self._fix_account_summary_formulas,
            self._revert_hierarchy_fix,
            self._setup_total_rec_pay_children,
        ]:
            try:
                with self.env.cr.savepoint():
                    method()
            except Exception as e:
                _logger.error(
                    'iman_account_summary: Error in %s (rolled back to savepoint): %s',
                    method.__name__, e
                )

    # ────────────────────────────────────────────────────────────────────────
    # Fix 1: Update formula + subformula for acc_rec & acc_pay
    # ────────────────────────────────────────────────────────────────────────
    def _fix_account_summary_formulas(self):
        """Update ACCOUNT RECEIVABLES and ACCOUNT PAYABLES to match Partner Ledger.
        acc_rec → asset_receivable (non_trade=False) → 'sum' → POSITIVE (+) Partner Ledger values
        acc_pay → liability_payable (non_trade=False) → 'sum' → NEGATIVE (-) Partner Ledger values
        """
        try:
            reports = self._get_account_summary_reports()
            total_updated = 0

            for report in reports:
                for code, (formula, subformula) in FORMULA_FIXES.items():
                    line = self._find_line(report, code)
                    if not line:
                        continue

                    expr = self.env['account.report.expression'].search([
                        ('report_line_id', '=', line.id),
                        ('label', '=', 'balance'),
                    ], limit=1)
                    if not expr:
                        continue

                    # Always force-update to ensure correct formula and sign are applied
                    expr.sudo().write({'formula': formula, 'subformula': subformula})
                    total_updated += 1
                    _logger.info(
                        'iman_account_summary: Set "%s" subformula="%s" in "%s".',
                        code, subformula, report.name
                    )

            _logger.info('iman_account_summary: Formula fix done (%s updated).', total_updated)

        except Exception as e:
            _logger.error('iman_account_summary: Error in _fix_account_summary_formulas: %s', e)

    # ────────────────────────────────────────────────────────────────────────
    # Fix 2: Restore acc_rec and acc_pay to top-level (no parent)
    # ────────────────────────────────────────────────────────────────────────
    def _revert_hierarchy_fix(self):
        """
        Restore ACCOUNT RECEIVABLES and ACCOUNT PAYABLES to top-level.
        """
        try:
            reports = self._get_account_summary_reports()

            for report in reports:
                for code, seq in [('acc_rec', 1), ('acc_pay', 7)]:
                    line = self._find_line(report, code)
                    if line and line.parent_id:
                        line.sudo().write({'parent_id': False, 'sequence': seq})
                        _logger.info(
                            'iman_account_summary: Restored "%s" to top-level '
                            '(seq=%s) in "%s".', code, seq, report.name
                        )

                # Restore tot_sales sequence if it was pushed
                tot = self._find_line(report, 'tot_sales')
                if tot and tot.sequence > 15 and tot.sequence < 9000:
                    tot.sudo().write({'sequence': 10})

        except Exception as e:
            _logger.error('iman_account_summary: Error in _revert_hierarchy_fix: %s', e)

    # ────────────────────────────────────────────────────────────────────────
    # Fix 3: Setup 'Total Receivable/Payable' as bold foldable parent
    #         with 'Total Receivables' and 'Total Payables' as children
    # ────────────────────────────────────────────────────────────────────────
    def _setup_total_rec_pay_children(self):
        """
        Find or create 'Total Receivable/Payable' line, make it foldable (bold),
        create two child lines underneath it, and set an aggregation
        expression on the parent so it shows the NET value (matching
        Partner Ledger total = receivables + payables combined).
        """
        try:
            reports = self._get_account_summary_reports()

            for report in reports:
                # ── 1. Clean up previously generated child lines ───────────
                bad_children = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    '|',
                    ('code', 'in', ['tot_rec_sub', 'tot_pay_sub']),
                    '&', ('name', '=', 'Receivables / Payables'), ('parent_id', '!=', False)
                ])
                if bad_children:
                    bad_children.sudo().unlink()
                    _logger.info('iman_account_summary: Cleaned up %s old child lines.', len(bad_children))

                # ── 2. Find or create parent line ──────────────────────────
                parent_line = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    '|', '|', '|',
                    ('code', '=', 'tot_rec_pay_parent'),
                    ('name', 'ilike', 'Total Receivable'),
                    ('name', 'ilike', 'Receivable/Payable'),
                    ('name', 'ilike', 'Receivables / Payables'),
                ], limit=1)

                if not parent_line:
                    _logger.info('iman_account_summary: Creating "Total Receivable/Payable" parent line in "%s".', report.name)
                    parent_line = self.env['account.report.line'].sudo().create({
                        'report_id': report.id,
                        'name': 'Total Receivable/Payable',
                        'code': 'tot_rec_pay_parent',
                        'sequence': 8,
                        'foldable': True,
                        'hide_if_zero': False,
                    })
                else:
                    parent_line.sudo().write({
                        'name': 'Total Receivable/Payable',
                        'foldable': True,
                        'code': 'tot_rec_pay_parent',
                    })

                parent_seq = parent_line.sequence

                # Remove any existing parent expressions (will recreate below)
                parent_exprs = self.env['account.report.expression'].search([
                    ('report_line_id', '=', parent_line.id)
                ])
                if parent_exprs:
                    parent_exprs.sudo().unlink()

                # ── 3. Create / update child lines ─────────────────────────
                for child_def in CHILD_LINES:
                    child_seq = parent_seq + 10 + child_def['sequence_offset']

                    child_line = self.env['account.report.line'].search([
                        ('report_id', '=', report.id),
                        ('code', '=', child_def['code']),
                    ], limit=1)

                    if child_line:
                        child_line.sudo().write({
                            'name': child_def['name'],
                            'parent_id': parent_line.id,
                            'sequence': child_seq,
                            'foldable': child_def['foldable'],
                            'hide_if_zero': child_def['hide_if_zero'],
                        })
                    else:
                        child_line = self.env['account.report.line'].sudo().create({
                            'report_id': report.id,
                            'name': child_def['name'],
                            'code': child_def['code'],
                            'parent_id': parent_line.id,
                            'sequence': child_seq,
                            'foldable': child_def['foldable'],
                            'hide_if_zero': child_def['hide_if_zero'],
                        })

                    _logger.info(
                        'iman_account_summary: Configured child "%s" (subformula=%s) under "%s".',
                        child_def['name'], child_def['subformula'], parent_line.name
                    )

                    child_expr = self.env['account.report.expression'].search([
                        ('report_line_id', '=', child_line.id),
                        ('label', '=', 'balance'),
                    ], limit=1)

                    if child_expr:
                        child_expr.sudo().write({
                            'engine': 'domain',
                            'formula': child_def['formula'],
                            'subformula': child_def['subformula'],
                            'date_scope': 'strict_range',
                        })
                    else:
                        self.env['account.report.expression'].sudo().create({
                            'report_line_id': child_line.id,
                            'label': 'balance',
                            'engine': 'domain',
                            'formula': child_def['formula'],
                            'subformula': child_def['subformula'],
                            'date_scope': 'strict_range',
                        })

                # ── 4. Add aggregation expression to parent ────────────────
                # Parent displays total in front of 'Total Receivable/Payable':
                # NET = Total Receivables (+) + Total Payables (-)
                self.env['account.report.expression'].sudo().create({
                    'report_line_id': parent_line.id,
                    'label': 'balance',
                    'engine': 'aggregation',
                    'formula': '-(tot_rec_sub.balance + tot_pay_sub.balance)',
                    'subformula': False,
                    'date_scope': 'strict_range',
                })
                _logger.info(
                    'iman_account_summary: Added aggregation expression to '
                    '"Total Receivable/Payable" parent (NET = receivables + payables).'
                )

                # ── 5. Move 'Total' (tot_sales) to LAST position ──────────
                tot_line = self._find_line(report, 'tot_sales')
                if tot_line and tot_line.sequence < 9000:
                    tot_line.sudo().write({'sequence': 9999})
                    _logger.info('iman_account_summary: Moved "Total" to sequence 9999.')

        except Exception as e:
            _logger.error(
                'iman_account_summary: Error in _setup_total_rec_pay_children: %s', e
            )

    # ────────────────────────────────────────────────────────────────────────
    # Helpers
    # ────────────────────────────────────────────────────────────────────────
    def _get_account_summary_reports(self):
        return self.env['account.report'].search([('name', 'like', 'Account Summary')])

    def _find_line(self, report, code):
        return self.env['account.report.line'].search([
            ('report_id', '=', report.id),
            ('code', '=', code),
        ], limit=1)
