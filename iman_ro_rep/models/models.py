from odoo import models, fields, api, exceptions
from num2words import num2words
# import inflect



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    check_tax = fields.Float(
        string='tax amt', compute='get_tax',
        required=False, store=True)

    tax_id_num = fields.Char(
        compute='cal_tax_val'
    )

    @api.depends('tax_ids')
    def cal_tax_val(self):
        for rec in self:
            rec.tax_id_num = ', '.join([(str(x.amount)+' %') for x in rec.tax_ids])

    @api.depends('tax_ids.amount', 'price_subtotal')
    def get_tax(self):
        for item in self:
            for tax in item.tax_ids:
                tax_amount = (item.price_subtotal * tax.amount) / 100
                # print(tax_amount)
                total_tax = tax_amount
                # print(total_tax)
                item.check_tax = total_tax


class AccountMoveNumWords(models.Model):
    _inherit = 'account.move'

    total_in_words = fields.Char(compute='int_to_words')

    @api.depends('amount_total')
    def int_to_words(self):
        for rec in self:
        #     # print(rec.amount_total)
        #     # print(int(rec.amount_total))
        #     rec.total_in_words = num2words(int(rec.amount_total), lang='en_US')
            rec.total_in_words = num2words(rec.amount_total, lang='en_US')
        #     # print(rec.total_in_words)

    # def number_to_words(amount_total):
    #     p = inflect.engine()
    #     return p.number_to_words(amount_total)

#
# class SaleOrderInherit(models.Model):
#     _inherit = 'sale.order'
#
#     @api.constrains('order_line.product_uom_qty')
#     def _check_order_lines_quantity(self):
#         for order in self:
#             for line in order.order_line:
#                 if line.product_uom_qty <= 0:
#                     raise exceptions.ValidationError("Quantity on sale order line must be greater than 0.")
#
#     def action_confirm(self):
#         for order in self:
#             for line in order.order_line:
#                 if line.product_uom_qty <= 0:
#                     raise exceptions.ValidationError("Quantity on sale order line must be greater than 0.")
#         res = super(SaleOrderInherit, self).action_confirm()
#         return res
#
