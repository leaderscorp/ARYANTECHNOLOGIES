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
    # @api.depends('default_account_id')
    # def _compute_balance_gl(self):
    #     for rec in self:
    #         account_lines = self.env['account.move.line'].search([('parent_state', '=', 'posted'), ('account_id', 'ilike', rec.default_account_id.code)])
    #         # account_lines = self.env['account.move.line'].search([('parent_state', '=', 'posted'), ('journal_id', '=', rec.id)])
    #         balance = 0
    #         curr_id = None
    #         for line in account_lines:
    #             balance += line.amount_currency
    #             curr_id = line.currency_id.symbol
    #         rec.balance_gl = balance
    #         rec.amount_currency_symbol= curr_id

    @api.depends('default_account_id')
    def _compute_balance_gl(self):
        """Batch version - highly efficient"""
        accounts = self.mapped('default_account_id')
        
        if not accounts:
            self.balance_gl = 0.0
            self.amount_currency_symbol = False
            return

        # One single query for ALL accounts
        self.env.cr.execute("""
            SELECT 
                aml.account_id,
                COALESCE(SUM(aml.amount_currency), 0) AS balance,
                MIN(cur.symbol) AS currency_symbol
            FROM account_move_line aml
            JOIN account_move am ON am.id = aml.move_id
            LEFT JOIN res_currency cur ON cur.id = aml.currency_id
            WHERE am.state = 'posted'
            AND aml.account_id IN %s
            AND aml.company_id = %s
            GROUP BY aml.account_id
        """, (tuple(accounts.ids), self.env.company.id))

        balance_dict = {}
        symbol_dict = {}
        for account_id, balance, symbol in self.env.cr.fetchall():
            balance_dict[account_id] = balance
            symbol_dict[account_id] = symbol

        # Assign values
        for rec in self:
            acc_id = rec.default_account_id.id
            rec.balance_gl = balance_dict.get(acc_id, 0.0)
            rec.amount_currency_symbol = symbol_dict.get(acc_id)
            
    def action_open_balance_gl(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("account_reports.action_account_report_general_ledger")

        action['context'] = dict(ast.literal_eval(action['context']), default_filter_accounts=self.default_account_id.code)

        return action