# -*- coding: utf-8 -*-
from odoo import models
import logging

_logger = logging.getLogger(__name__)

# ── Formula fixes for top-level lines ──────────────────────────────────────
# {line_code: (formula, subformula)}
FORMULA_FIXES = {
    # ACCOUNT RECEIVABLES → full account 110000 (same as Balance Sheet)
    'acc_rec': ("[('account_id.code', '=', 110000)]", 'sum'),

    # ACCOUNT PAYABLES → full account 610000 (same as Balance Sheet)
    # '-sum' flips sign to match Balance Sheet negative display
    'acc_pay': ("[('account_id.code', '=', 610000)]", '-sum'),
}

# ── Child lines to create under 'Total Receivable/Payable' ─────────────────
# Same formulas as Balance Sheet 'Total Receivables' and 'Total Payables'
CHILD_LINES = [
    {
        'name': 'Total Receivables',
        'code': 'tot_rec_sub',
        'sequence_offset': 1,      # parent_seq + 1
        'foldable': False,
        'hide_if_zero': False,
        'formula': "[('account_id.account_type', '=', 'asset_receivable'), ('account_id.non_trade', '=', False)]",
        'subformula': 'sum',       # same as Balance Sheet Total Receivables
    },
    {
        'name': 'Total Payables',
        'code': 'tot_pay_sub',
        'sequence_offset': 2,      # parent_seq + 2
        'foldable': False,
        'hide_if_zero': False,
        'formula': "[('account_id.account_type', '=', 'liability_payable'), ('account_id.non_trade', '=', False)]",
        'subformula': '-sum',      # same as Balance Sheet Total Payables
    },
]


class ImanAccountSummaryFix(models.AbstractModel):
    """
    Runs on every module install/upgrade to fix Account Summary report:

    1. FORMULA FIX:
       - ACCOUNT RECEIVABLES (acc_rec): full account 110000 balance
       - ACCOUNT PAYABLES (acc_pay): full account 610000 balance with sign fix

    2. REVERT: Restore acc_rec and acc_pay to top-level (no parent_id)
       (undoes a previous mistaken hierarchy change)

    3. TOTAL Receivable/Payable CHILDREN:
       - Make 'Total Receivable/Payable' foldable (bold, expandable)
       - Add 'Total Receivables' child  → same as Balance Sheet Total Receivables
       - Add 'Total Payables' child     → same as Balance Sheet Total Payables
       When user expands 'Total Receivable/Payable', they see both totals.
    """
    _name = 'iman.account.summary.fix'
    _description = 'Iman Account Summary Formula Fix'

    def _register_hook(self):
        super()._register_hook()
        self._fix_account_summary_formulas()
        self._revert_hierarchy_fix()
        self._setup_total_rec_pay_children()

    # ────────────────────────────────────────────────────────────────────────
    # Fix 1: Update formula + subformula for acc_rec & acc_pay
    # ────────────────────────────────────────────────────────────────────────
    def _fix_account_summary_formulas(self):
        """Update ACCOUNT RECEIVABLES and ACCOUNT PAYABLES to match Balance Sheet."""
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

                    if expr.formula != formula or expr.subformula != subformula:
                        expr.sudo().write({'formula': formula, 'subformula': subformula})
                        total_updated += 1
                        _logger.info(
                            'iman_account_summary: Updated expression for "%s" in "%s".',
                            code, report.name
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
        A previous version of this module mistakenly moved them as children
        which hid them from the top of the report.
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
                if tot and tot.sequence > 15:
                    tot.sudo().write({'sequence': 10})

        except Exception as e:
            _logger.error('iman_account_summary: Error in _revert_hierarchy_fix: %s', e)

    # ────────────────────────────────────────────────────────────────────────
    # Fix 3: Setup 'Total Receivable/Payable' as bold foldable parent
    #         with 'Total Receivables' and 'Total Payables' as children
    # ────────────────────────────────────────────────────────────────────────
    def _setup_total_rec_pay_children(self):
        """
        Find 'Total Receivable/Payable' line, make it foldable (bold),
        and create/update two child lines underneath it:
          - Total Receivables  → Balance Sheet formula (all receivable accounts)
          - Total Payables     → Balance Sheet formula (all payable accounts)

        The top-level ACCOUNT RECEIVABLES and ACCOUNT PAYABLES are untouched.
        """
        try:
            reports = self._get_account_summary_reports()

            for report in reports:
                # ── Find 'Total Receivable/Payable' parent line ────────────
                parent_line = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    ('code', 'not in', ['tot_rec_sub', 'tot_pay_sub']), # Prevent matching our own children
                    '|',
                    ('name', 'ilike', 'Total Receivable'),
                    ('name', 'ilike', 'Receivable/Payable'),
                ], limit=1)

                if not parent_line:
                    _logger.warning(
                        'iman_account_summary: "Total Receivable/Payable" not found '
                        'in report "%s". Skipping child setup.', report.name
                    )
                    continue

                parent_seq = parent_line.sequence

                # ── Make parent NOT foldable (acts as permanent header) ──────
                # Odoo automatically adds a "Total [Parent Name]" line at the bottom
                # when a parent is foldable. Setting foldable=False removes that extra total line.
                if parent_line.foldable:
                    parent_line.sudo().write({'foldable': False})
                    _logger.info(
                        'iman_account_summary: Set foldable=False on "%s".',
                        parent_line.name
                    )

                # ── Rename parent to fix 'Total Total...' issue ─────────────
                # Odoo automatically adds 'Total ' to the parent name when expanded.
                # Renaming it to 'Receivables / Payables' makes the bottom line
                # 'Total Receivables / Payables' which looks correct.
                if 'Total' in parent_line.name:
                    parent_line.sudo().write({'name': 'Receivables / Payables'})
                    _logger.info('iman_account_summary: Renamed parent to "Receivables / Payables".')

                # ── Create/update child lines ──────────────────────────────
                for child_def in CHILD_LINES:
                    child_seq = parent_seq + child_def['sequence_offset']

                    # Check if child already exists (by code)
                    existing = self.env['account.report.line'].search([
                        ('report_id', '=', report.id),
                        ('code', '=', child_def['code']),
                    ], limit=1)

                    if existing:
                        # Update existing child
                        existing.sudo().write({
                            'parent_id': parent_line.id,  # RESTORE parent_id
                            'sequence': child_seq,
                        })
                        child_line = existing
                        _logger.info(
                            'iman_account_summary: Updated child "%s" under "%s".',
                            child_def['name'], parent_line.name
                        )
                    else:
                        # Create new child line
                        child_line = self.env['account.report.line'].sudo().create({
                            'report_id': report.id,
                            'name': child_def['name'],
                            'code': child_def['code'],
                            'parent_id': parent_line.id,  # RESTORE parent_id
                            'sequence': child_seq,
                            'foldable': child_def['foldable'],
                            'hide_if_zero': child_def['hide_if_zero'],
                        })
                        _logger.info(
                            'iman_account_summary: Created child "%s" under "%s".',
                            child_def['name'], parent_line.name
                        )

                    # ── Create/update the expression for child line ────────
                    expr = self.env['account.report.expression'].search([
                        ('report_line_id', '=', child_line.id),
                        ('label', '=', 'balance'),
                    ], limit=1)

                    if expr:
                        if (expr.formula != child_def['formula'] or
                                expr.subformula != child_def['subformula']):
                            expr.sudo().write({
                                'formula': child_def['formula'],
                                'subformula': child_def['subformula'],
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
                        _logger.info(
                            'iman_account_summary: Created expression for "%s".',
                            child_def['name']
                        )

                # ── Move 'Total' (tot_sales) to LAST position ─────────────
                # User wants grand total at the very end, after this section
                tot_line = self._find_line(report, 'tot_sales')
                if tot_line:
                    # tot_sales must come AFTER all children of parent_line
                    last_child_seq = parent_seq + len(CHILD_LINES)
                    if tot_line.sequence <= last_child_seq:
                        tot_line.sudo().write({'sequence': last_child_seq + 10})
                        _logger.info(
                            'iman_account_summary: Moved "Total" (tot_sales) to '
                            'last position (seq=%s) in "%s".',
                            last_child_seq + 10, report.name
                        )

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
