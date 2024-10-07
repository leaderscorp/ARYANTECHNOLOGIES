from odoo import api, fields, models
import datetime
import pytz


class AtPartnerLedgerCurrRep(models.TransientModel):
    #
    _name = 'at.partner.ledger.currency.report'
    _description = 'at.partner.ledger.currency.report'

    start_date = fields.Date(string='From Date', store=True)
    end_date = fields.Date(string='To Date', store=True)

    partner_id_name = fields.Many2many(
        comodel_name='res.partner',
        string="Partner's Name",
        required='True')

    partner_id_curr = fields.Many2many(
        comodel_name='res.currency',
        string='Currency',
        required='True')

    partner_account = fields.Selection(
        string='Partner Account',
        selection=[('asset_receivable', 'Receivable Accounts'),
                   ('liability_payable', 'Payable Accounts'),
                   ('both', 'Receivable And Payable Accounts')],
        required=False, )

    def get_curr_rep_xlsx(self):
        selection = ['asset_receivable', 'liability_payable'] if self.partner_account == 'both' else [
            self.partner_account]


        domain_og = [
            # ('display_type', 'not in', ('line_section', 'line_note')),
            ('currency_id', 'in', self.partner_id_curr.ids),
            ('partner_id', 'in', self.partner_id_name.ids),
            ('create_date', '>=', self.start_date),
            ('create_date', '<=', self.end_date)
        ]
        add_domain = [
            ('account_id.account_type', 'in', selection),
            ('account_id.non_trade', '=', False), ]
        if selection == [False]:
            domain = domain_og
        else:
            domain = domain_og + add_domain
        dic = {}
        lines = self.env['account.move.line'].search(domain, order='matching_number')
        for rec in lines:
            dic[rec.id] = {
                'currency': rec.currency_id.name,
                'matching_number': rec.matching_number if rec.matching_number else None,
                'partner': rec.partner_id.name,
                'debit': rec.debit,
                'credit': rec.credit,
                'reference': rec.move_name,
                'name': rec.name,
                'balance': rec.balance,
                'currency_rate': rec.currency_rate,
            }

        data = {'data': dic}

        return self.env.ref('at_prtnr_ledg_curr_rep.partner_ledger_currency_report_action').report_action(self,
                                                                                                          data=data)

        # print([x.credit for x in t])

    # def get_rep_xlsx(self):
    #     if self.name_sequence == 'New':
    #         self.name_sequence = self.env['ir.sequence'].next_by_code('gatepass.reference.seq') or 'New'
    #     else:
    #         pass
    #
    #     inv_data_dict = {}
    #     if self._context.get('active_model') == 'account.move':
    #         test = self.env['account.move'].browse(self._context.get('active_ids', []))
    #     else:
    #         pass
    #
    #     self._cr.execute(f"""
    #         select
    #         product_id,
    #         sum(quantity) as p_quantity
    #         from
    #         account_move_line
    #         where move_id in %s
    #         and product_id is not null
# 	    group by product_id""", [tuple(test.mapped('id'))])
#
#     qdata = self._cr.dictfetchall()
#     sum = 0
#     for data in qdata:
#         packaging = self.env['product.packaging'].search([('product_id', '=', data.get('product_id'))], limit=1).qty
#         sum += data['p_quantity']
#         inv_data_dict[data.get('product_id')] = {
#             'name': self.env['product.product'].browse(data.get('product_id')).name,
#             'packaging': None if packaging == False else data['p_quantity']/packaging,
#             'qty': data['p_quantity'],
#         }
#     user_tz = self.env.user.tz
#     cur_time = datetime.datetime.now(tz=pytz.timezone(user_tz))
#     date_format = '%d/%m/%Y %I:%M:%S %p'
#     data = {
#         # 'mk_gp_list': inv_data_dict,
#         # 'date': cur_time.strftime(date_format),
#         # 'inv_count': len(test.mapped('name')),
#         # 'inv_name': ', '.join(test.mapped('name')),
#         # 'form_d': self.read()[0],
#         # 'total': sum
#     }
#     return self.env.ref('mk_wizard_rep.gate_pass_report_template_action').report_action(self, data=data)
