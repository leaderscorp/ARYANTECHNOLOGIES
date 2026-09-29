# -*- coding: utf-8 -*-
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

# Target formula: same as Balance Sheet Account Receivable line
# This shows the full account 110000 balance without any partner exclusions
TARGET_FORMULA = "[('account_id.code', '=', 110000)]"


class ImanAccountSummaryFix(models.AbstractModel):
    """
    This model uses _register_hook to update the 'ACCOUNT RECEIVABLES' line
    in the Account Summary report on every module install/upgrade.

    The fix changes the formula from:
        [account_id.code=110000 excluding EMPLOYEE & RELATED PARTY]
    To:
        [account_id.code=110000] (full balance, same as Balance Sheet)
    """
    _name = 'iman.account.summary.fix'
    _description = 'Iman Account Summary Formula Fix'

    def _register_hook(self):
        super()._register_hook()
        self._fix_account_receivables_formula()

    def _fix_account_receivables_formula(self):
        """
        Update the ACCOUNT RECEIVABLES expression in all Account Summary reports
        to match the Balance Sheet's Account Receivable (account 110000) value.
        """
        try:
            # Search for Account Summary reports (there may be multiple for different companies)
            reports = self.env['account.report'].search([
                ('name', 'like', 'Account Summary')
            ])

            if not reports:
                _logger.warning(
                    'iman_account_summary: No "Account Summary" report found. '
                    'Could not update ACCOUNT RECEIVABLES formula.'
                )
                return

            updated = 0
            for report in reports:
                # Find the ACCOUNT RECEIVABLES line (code = acc_rec)
                line = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    ('code', '=', 'acc_rec'),
                ], limit=1)

                if not line:
                    continue

                # Find the 'balance' expression for this line
                expr = self.env['account.report.expression'].search([
                    ('report_line_id', '=', line.id),
                    ('label', '=', 'balance'),
                ], limit=1)

                if not expr:
                    continue

                if expr.formula != TARGET_FORMULA:
                    expr.sudo().write({'formula': TARGET_FORMULA})
                    updated += 1
                    _logger.info(
                        'iman_account_summary: Updated ACCOUNT RECEIVABLES formula '
                        'in report "%s" (id=%s). Old formula replaced with: %s',
                        report.name, report.id, TARGET_FORMULA
                    )

            if updated:
                _logger.info(
                    'iman_account_summary: Successfully updated %s report(s).', updated
                )
            else:
                _logger.info(
                    'iman_account_summary: No updates needed - formula already correct.'
                )

        except Exception as e:
            _logger.error(
                'iman_account_summary: Error updating ACCOUNT RECEIVABLES formula: %s', str(e)
            )
