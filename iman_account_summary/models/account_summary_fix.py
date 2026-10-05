# -*- coding: utf-8 -*-
from odoo import models
import logging

_logger = logging.getLogger(__name__)

# ── Formula fixes for top-level lines ──────────────────────────────────────
# {line_code: (formula, subformula)}
FORMULA_FIXES = {
    # ACCOUNT RECEIVABLES → Partner Ledger style (asset_receivable accounts)
    # 'sum' gives positive values (Debit - Credit) matching Partner Ledger
    'acc_rec': ("[('account_id.account_type', '=', 'asset_receivable'), ('account_id.non_trade', '=', False)]", 'sum'),

    # ACCOUNT PAYABLES → Partner Ledger style (liability_payable accounts)
    # '-sum' flips sign to show negative values matching Partner Ledger
    'acc_pay': ("[('account_id.account_type', '=', 'liability_payable'), ('account_id.non_trade', '=', False)]", '-sum'),
}

# ── Child lines to create under 'Total Receivable/Payable' ─────────────────
# Same formulas as Partner Ledger - Total Receivables & Total Payables
CHILD_LINES = [
    {
        'name': 'Total Receivables',
        'code': 'tot_rec_sub',
        'sequence_offset': 1,      # parent_seq + 1
        'foldable': False,
        'hide_if_zero': False,
        'formula': "[('account_id.account_type', '=', 'asset_receivable'), ('account_id.non_trade', '=', False)]",
        'subformula': 'sum',       # Partner Ledger style: positive (Debit - Credit)
    },
    {
        'name': 'Total Payables',
        'code': 'tot_pay_sub',
        'sequence_offset': 2,      # parent_seq + 2
        'foldable': False,
        'hide_if_zero': False,
        'formula': "[('account_id.account_type', '=', 'liability_payable'), ('account_id.non_trade', '=', False)]",
        'subformula': '-sum',      # Partner Ledger style: negative (Credit - Debit)
    },
]


class ImanAccountSummaryFix(models.AbstractModel):
    """
    Runs on every module install/upgrade to fix Account Summary report:

    1. FORMULA FIX (Partner Ledger style):
       - ACCOUNT RECEIVABLES (acc_rec): asset_receivable accounts, 'sum'
         → Shows POSITIVE values (same as Partner Ledger)
       - ACCOUNT PAYABLES (acc_pay): liability_payable accounts, '-sum'
         → Shows NEGATIVE values (same as Partner Ledger)

    2. REVERT: Restore acc_rec and acc_pay to top-level (no parent_id)
       (undoes a previous mistaken hierarchy change)

    3. TOTAL Receivable/Payable CHILDREN:
       - Make 'Total Receivable/Payable' foldable (bold, expandable)
       - Add 'Total Receivables' child  → Partner Ledger Total Receivables (positive)
       - Add 'Total Payables' child     → Partner Ledger Total Payables (negative)
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
        """Update ACCOUNT RECEIVABLES and ACCOUNT PAYABLES to match Partner Ledger.

        Account Receivable: asset_receivable accounts with 'sum' → positive values
        Account Payable: liability_payable accounts with '-sum' → negative values
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
        and create/update two child lines underneath it.
        To avoid the 'Total Total...' bottom line generated by Odoo,
        we remove the expression from the parent line so it has no value.
        """
        try:
            reports = self._get_account_summary_reports()

            for report in reports:
                # ── 1. Clean up corrupted child lines ─────────────────────
                # Remove any previously generated children or corrupted lines
                # that were accidentally renamed to 'Receivables / Payables'
                bad_children = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    '|',
                    ('code', 'in', ['tot_rec_sub', 'tot_pay_sub']),
                    '&', ('name', '=', 'Receivables / Payables'), ('parent_id', '!=', False)
                ])
                if bad_children:
                    bad_children.sudo().unlink()
                    _logger.info('iman_account_summary: Cleaned up %s corrupted child lines.', len(bad_children))

                # ── 2. Find parent line ────────────────────────────────────
                # The real parent must be top-level (no parent_id)
                parent_line = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    ('parent_id', '=', False),
                    '|', '|',
                    ('name', 'ilike', 'Total Receivable'),
                    ('name', 'ilike', 'Receivable/Payable'),
                    ('name', 'ilike', 'Receivables / Payables'),
                ], limit=1)

                if not parent_line:
                    _logger.warning(
                        'iman_account_summary: "Total Receivable/Payable" not found '
                        'in report "%s". Skipping child setup.', report.name
                    )
                    continue

                parent_seq = parent_line.sequence

                # ── 3. Restore Parent & Remove Expression ──────────────────
                # Make parent foldable so it's clickable.
                # Rename it back to what the user expects.
                parent_line.sudo().write({
                    'name': 'Total Receivable/Payable',
                    'foldable': True,
                    'code': 'tot_rec_pay_parent', # Assign code for future safety
                })
                
                # Odoo adds 'Total <Name>' at the bottom of a foldable section
                # ONLY IF the parent line computes a value.
                # By removing its expressions, it becomes purely a visual folder,
                # avoiding the 'Total Total Receivable/Payable' issue completely!
                parent_exprs = self.env['account.report.expression'].search([
                    ('report_line_id', '=', parent_line.id)
                ])
                if parent_exprs:
                    parent_exprs.sudo().unlink()
                    _logger.info('iman_account_summary: Removed expressions from parent line to prevent bottom total.')

                # ── 4. Create child lines ──────────────────────────────────
                for child_def in CHILD_LINES:
                    # Give children a significantly higher sequence
                    child_seq = parent_seq + 10 + child_def['sequence_offset']

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
                        'iman_account_summary: Created child "%s" under "%s".',
                        child_def['name'], parent_line.name
                    )

                    self.env['account.report.expression'].sudo().create({
                        'report_line_id': child_line.id,
                        'label': 'balance',
                        'engine': 'domain',
                        'formula': child_def['formula'],
                        'subformula': child_def['subformula'],
                        'date_scope': 'strict_range',
                    })

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
