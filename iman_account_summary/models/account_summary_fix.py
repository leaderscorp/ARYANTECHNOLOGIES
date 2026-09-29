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
    This model uses _register_hook to update line formulas in Account Summary
    report on every module install/upgrade.

    Fixes:
    - ACCOUNT RECEIVABLES: removes EMPLOYEE/RELATED PARTY partner filter
      → shows full account 110000 balance (matches Balance Sheet)
    - ACCOUNT PAYABLES: removes EMPLOYEE/RELATED PARTY partner filter
      → shows full account 610000 balance (matches Balance Sheet)
    """
    _name = 'iman.account.summary.fix'
    _description = 'Iman Account Summary Formula Fix'

    def _register_hook(self):
        super()._register_hook()
        self._fix_account_summary_formulas()

    def _fix_account_summary_formulas(self):
        """
        Update ACCOUNT RECEIVABLES and ACCOUNT PAYABLES expressions in all
        Account Summary reports to match Balance Sheet values.
        """
        try:
            # Search for all Account Summary reports
            reports = self.env['account.report'].search([
                ('name', 'like', 'Account Summary')
            ])

            if not reports:
                _logger.warning(
                    'iman_account_summary: No "Account Summary" report found.'
                )
                return

            total_updated = 0

            for report in reports:
                for line_code, (target_formula, target_subformula) in FORMULA_FIXES.items():

                    # Find the line by code
                    line = self.env['account.report.line'].search([
                        ('report_id', '=', report.id),
                        ('code', '=', line_code),
                    ], limit=1)

                    if not line:
                        continue

                    # Find the 'balance' expression
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
                        old_formula = expr.formula
                        old_subformula = expr.subformula
                        expr.sudo().write({
                            'formula': target_formula,
                            'subformula': target_subformula,
                        })
                        total_updated += 1
                        _logger.info(
                            'iman_account_summary: Updated line "%s" (code=%s) '
                            'in report "%s" (id=%s).'
                            '\n  Old formula: %s | subformula: %s'
                            '\n  New formula: %s | subformula: %s',
                            line.name, line_code, report.name, report.id,
                            old_formula, old_subformula,
                            target_formula, target_subformula
                        )

            if total_updated:
                _logger.info(
                    'iman_account_summary: Total %s expression(s) updated.', total_updated
                )
            else:
                _logger.info(
                    'iman_account_summary: All formulas already correct - no update needed.'
                )

        except Exception as e:
            _logger.error(
                'iman_account_summary: Error updating formulas: %s', str(e)
            )
