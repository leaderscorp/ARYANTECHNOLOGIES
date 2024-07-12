# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockQuants(models.Model):
    _inherit = 'stock.quant'

    im_value = fields.Float(compute='_get_value', store=True)
    im_avg_cost = fields.Float(compute='_get_value', store=True)
    im_prod_tag = fields.Char(compute='_get_value', store=True)

    @api.depends('value', 'quantity', 'product_id.im_product_tag')
    def _get_value(self):
        for rec in self:
            rec.im_value = rec.value
            rec.im_prod_tag = rec.product_id.im_product_tag
            if rec.quantity == 0:
                rec.im_avg_cost = 0
            else:
                rec.im_avg_cost = (rec.value/rec.quantity)
    

