from collections import defaultdict
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import ast

class AccountJournalInherit(models.Model):
    _inherit = 'account.journal'

    # amount_currency_symbol = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)
    balance_gl = fields.Monetary(string='Balance GL', compute="_compute_balance_gl")
    amount_currency_symbol = fields.Char()


    # , ('move_name', 'ilike', rec.code),
    def _compute_balance_gl(self):
        for rec in self:
            account_lines = self.env['account.move.line'].search([('parent_state', '=', 'posted'), ('account_id', 'ilike', rec.default_account_id.code)])
            # account_lines = self.env['account.move.line'].search([('parent_state', '=', 'posted'), ('journal_id', '=', rec.id)])
            balance = 0
            curr_id = None
            for line in account_lines:
                balance += line.amount_currency
                curr_id = line.currency_id.symbol
            rec.balance_gl = balance
            rec.amount_currency_symbol= curr_id
    def action_open_balance_gl(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("account_reports.action_account_report_general_ledger")

        action['context'] = dict(ast.literal_eval(action['context']), default_filter_accounts=self.default_account_id.code)

        return action