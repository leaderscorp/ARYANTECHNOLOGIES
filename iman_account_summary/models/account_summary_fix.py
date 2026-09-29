# -*- coding: utf-8 -*-
from odoo import models
import logging

_logger = logging.getLogger(__name__)

# Lines to fix: {line_code: (formula, subformula)}
# Formula and subformula match the Balance Sheet for each account
FORMULA_FIXES = {
    # ACCOUNT RECEIVABLES → full account 110000 (same as Balance Sheet)
    # subformula 'sum' = debit - credit (negative when credit-heavy)
    'acc_rec': ("[('account_id.code', '=', 110000)]", 'sum'),

    # ACCOUNT PAYABLES → full account 610000 (same as Balance Sheet)
    # Balance Sheet uses '-sum' for payables: -(debit-credit) = credit-debit
    # This makes payable show as negative (matching Balance Sheet -665M)
    'acc_pay': ("[('account_id.code', '=', 610000)]", '-sum'),
}


class ImanAccountSummaryFix(models.AbstractModel):
    """
    This model uses _register_hook to:
    1. Fix ACCOUNT RECEIVABLES formula → full account 110000 (matches Balance Sheet)
    2. Fix ACCOUNT PAYABLES formula → full account 610000 (matches Balance Sheet)
    3. Make 'Total Receivable/Payable' line foldable (bold parent)
       → When clicked, shows ACCOUNT RECEIVABLES and ACCOUNT PAYABLES inside it
    """
    _name = 'iman.account.summary.fix'
    _description = 'Iman Account Summary Formula Fix'

    def _register_hook(self):
        super()._register_hook()
        self._fix_account_summary_formulas()
        self._fix_total_rec_pay_hierarchy()

    # ─────────────────────────────────────────────────────────
    # Fix 1: Update formula + subformula for acc_rec & acc_pay
    # ─────────────────────────────────────────────────────────
    def _fix_account_summary_formulas(self):
        """
        Update ACCOUNT RECEIVABLES and ACCOUNT PAYABLES expressions in all
        Account Summary reports to match Balance Sheet values.
        """
        try:
            reports = self.env['account.report'].search([
                ('name', 'like', 'Account Summary')
            ])

            if not reports:
                _logger.warning('iman_account_summary: No "Account Summary" report found.')
                return

            total_updated = 0

            for report in reports:
                for line_code, (target_formula, target_subformula) in FORMULA_FIXES.items():

                    line = self.env['account.report.line'].search([
                        ('report_id', '=', report.id),
                        ('code', '=', line_code),
                    ], limit=1)
                    if not line:
                        continue

                    expr = self.env['account.report.expression'].search([
                        ('report_line_id', '=', line.id),
                        ('label', '=', 'balance'),
                    ], limit=1)
                    if not expr:
                        continue

                    needs_update = (
                        expr.formula != target_formula or
                        expr.subformula != target_subformula
                    )
                    if needs_update:
                        expr.sudo().write({
                            'formula': target_formula,
                            'subformula': target_subformula,
                        })
                        total_updated += 1
                        _logger.info(
                            'iman_account_summary: Updated expression for line "%s" '
                            '(code=%s) in report "%s".',
                            line.name, line_code, report.name
                        )

            _logger.info(
                'iman_account_summary: Formula fix done. %s expression(s) updated.',
                total_updated
            )

        except Exception as e:
            _logger.error('iman_account_summary: Error in _fix_account_summary_formulas: %s', e)

    # ─────────────────────────────────────────────────────────
    # Fix 2: Make 'Total Receivable/Payable' a bold foldable parent
    #         ACCOUNT RECEIVABLES and ACCOUNT PAYABLES = children
    # ─────────────────────────────────────────────────────────
    def _fix_total_rec_pay_hierarchy(self):
        """
        Find the 'Total Receivable/Payable' line in each Account Summary report.
        - Make it foldable (acts as bold parent section)
        - Set ACCOUNT RECEIVABLES (acc_rec) and ACCOUNT PAYABLES (acc_pay)
          as child lines under it
        - When user clicks the parent, acc_rec and acc_pay expand inside it
        """
        try:
            reports = self.env['account.report'].search([
                ('name', 'like', 'Account Summary')
            ])
            if not reports:
                return

            for report in reports:
                # ── Find 'Total Receivable/Payable' parent line ──
                # Search by name (covers server variants of the name)
                parent_line = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    '|',
                    ('name', 'ilike', 'Total Receivable'),
                    ('name', 'ilike', 'Receivable/Payable'),
                ], limit=1)

                if not parent_line:
                    _logger.warning(
                        'iman_account_summary: Could not find "Total Receivable/Payable" '
                        'line in report "%s". Skipping hierarchy fix.', report.name
                    )
                    continue

                # ── Make parent foldable (shows as bold, expandable) ──
                if not parent_line.foldable:
                    parent_line.sudo().write({'foldable': True})
                    _logger.info(
                        'iman_account_summary: Set foldable=True on "%s" in report "%s".',
                        parent_line.name, report.name
                    )

                # ── Find acc_rec and acc_pay lines ──
                rec_line = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    ('code', '=', 'acc_rec'),
                ], limit=1)

                pay_line = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    ('code', '=', 'acc_pay'),
                ], limit=1)

                # ── Set acc_rec as child of parent ──
                if rec_line and rec_line.parent_id != parent_line:
                    rec_line.sudo().write({
                        'parent_id': parent_line.id,
                        'sequence': 0,
                        'foldable': True,   # still expandable for partner drill-down
                    })
                    _logger.info(
                        'iman_account_summary: Set "%s" as child of "%s" in report "%s".',
                        rec_line.name, parent_line.name, report.name
                    )

                # ── Set acc_pay as child of parent ──
                if pay_line and pay_line.parent_id != parent_line:
                    pay_line.sudo().write({
                        'parent_id': parent_line.id,
                        'sequence': 1,
                        'foldable': True,   # still expandable for partner drill-down
                    })
                    _logger.info(
                        'iman_account_summary: Set "%s" as child of "%s" in report "%s".',
                        pay_line.name, parent_line.name, report.name
                    )

        except Exception as e:
            _logger.error(
                'iman_account_summary: Error in _fix_total_rec_pay_hierarchy: %s', e
            )
