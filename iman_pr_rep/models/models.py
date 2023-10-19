# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words

class AccountPaymentsNumWords(models.Model):
    _inherit = 'account.payment'

    total_in_words = fields.Char(compute='int_to_words')

    @api.depends('amount_total')
    def int_to_words(self):
        for rec in self:
            rec.total_in_words = num2words(rec.amount, lang='en_US')

