# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words

class AccountPaymentsNumWords(models.Model):
    _inherit='repair.order'

    inv_name = fields.Char(string="Invoice Name", related='invoice_id.name')
    inv_date = fields.Date(string='Invoice Date' , related='invoice_id.invoice_date')


