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
          as child lines under it, with sequences AFTER the parent
        - Child sequence MUST be > parent sequence (Odoo requirement)
        """
        try:
            reports = self.env['account.report'].search([
                ('name', 'like', 'Account Summary')
            ])
            if not reports:
                return

            for report in reports:
                # ── Find 'Total Receivable/Payable' parent line ──
                parent_line = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    '|',
                    ('name', 'ilike', 'Total Receivable'),
                    ('name', 'ilike', 'Receivable/Payable'),
                ], limit=1)

                if not parent_line:
                    _logger.warning(
                        'iman_account_summary: "Total Receivable/Payable" not found '
                        'in report "%s". Skipping hierarchy fix.', report.name
                    )
                    continue

                parent_seq = parent_line.sequence  # e.g. 10

                # ── Make parent foldable (bold, expandable) ──
                parent_line.sudo().write({'foldable': True})

                # ── Find acc_rec and acc_pay lines ──
                rec_line = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    ('code', '=', 'acc_rec'),
                ], limit=1)

                pay_line = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    ('code', '=', 'acc_pay'),
                ], limit=1)

                # ── Set acc_rec as child with sequence AFTER parent ──
                # Odoo requires: child.sequence > parent.sequence
                if rec_line:
                    rec_line.sudo().write({
                        'parent_id': parent_line.id,
                        'sequence': parent_seq + 1,   # e.g. 11
                        'foldable': True,
                    })
                    _logger.info(
                        'iman_account_summary: "%s" → child of "%s" (seq=%s) in "%s".',
                        rec_line.name, parent_line.name, parent_seq + 1, report.name
                    )

                # ── Set acc_pay as child with sequence AFTER acc_rec ──
                if pay_line:
                    pay_line.sudo().write({
                        'parent_id': parent_line.id,
                        'sequence': parent_seq + 2,   # e.g. 12
                        'foldable': True,
                    })
                    _logger.info(
                        'iman_account_summary: "%s" → child of "%s" (seq=%s) in "%s".',
                        pay_line.name, parent_line.name, parent_seq + 2, report.name
                    )

                # ── Push 'Total' (tot_sales) sequence after children ──
                total_line = self.env['account.report.line'].search([
                    ('report_id', '=', report.id),
                    ('code', '=', 'tot_sales'),
                ], limit=1)
                if total_line and total_line.sequence <= parent_seq + 2:
                    total_line.sudo().write({'sequence': parent_seq + 10})
                    _logger.info(
                        'iman_account_summary: Moved "Total" (tot_sales) to seq=%s.',
                        parent_seq + 10
                    )

        except Exception as e:
            _logger.error(
                'iman_account_summary: Error in _fix_total_rec_pay_hierarchy: %s', e
            )

