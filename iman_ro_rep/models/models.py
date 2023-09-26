from num2words import num2words

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    check_tax = fields.Float(
        string='tax amt', compute='get_tax',
        required=False, store=True)

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

    total_in_words = fields.Char(compute='int_to_words', store=True)

    def int_to_words(self):
        for rec in self:
            # print(rec.amount_total)
            # print(int(rec.amount_total))
            rec.total_in_words = num2words(int(rec.amount_total), lang='en_US')
            # print(rec.total_in_words)