# -*- coding: utf-8 -*-

from odoo import models, fields, api


class im_mrp_production(models.Model):
    _inherit = 'mrp.production'

    im_product_tag = fields.Char(compute='_get_prod_tag', store=True)
    im_avg_cost = fields.Float(compute='_get_other_avg', store=True)
    im_qty = fields.Float(compute='_get_other_qty', store=True)
    im_total_val = fields.Float(compute='_get_other_total_val', store=True)

    @api.depends('product_tmpl_id.im_product_tag_p')
    def _get_prod_tag(self):
        for record in self:
            record.im_product_tag = record.product_tmpl_id.im_product_tag_p

    @api.depends('product_id.standard_price')
    def _get_other_avg(self):
        for record in self:
            record.im_avg_cost = record.product_id.standard_price

    @api.depends('product_id.qty_available')
    def _get_other_qty(self):
        for record in self:
            record.im_qty = record.product_id.qty_available

    @api.depends('product_id.qty_available', 'product_id.standard_price')
    def _get_other_total_val(self):
        for record in self:
            record.im_total_val = record.product_id.qty_available * record.product_id.standard_price
