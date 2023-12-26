from collections import defaultdict
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import ast

class AccountJournalInherit(models.Model):
    _inherit = 'account.journal'

    balance_gl = fields.Float(string='Balance GL', compute="_compute_balance_gl")
    # , ('move_name', 'ilike', rec.code), 
    def _compute_balance_gl(self):
        for rec in self:
            account_lines = self.env['account.move.line'].search([('parent_state', '=', 'posted'), ('account_id', 'ilike', rec.default_account_id.code)])
            balance = 0
            for line in account_lines:
                balance += line.balance
            rec.balance_gl = balance
    
    def action_open_balance_gl(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("account_reports.action_account_report_general_ledger")

        action['context'] = dict(ast.literal_eval(action['context']), default_filter_accounts=self.default_account_id.code)

        return action