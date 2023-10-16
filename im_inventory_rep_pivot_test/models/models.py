# -*- coding: utf-8 -*-

from odoo import models, fields, api


class im_inventory_product(models.Model):
    _inherit = 'product.template'

    im_product_tag_p = fields.Char(compute='_get_prod_tag_p')

    @api.depends('product_tag_ids.name')
    def _get_prod_tag_p(self):
        for record in self:
            record.im_product_tag_p = ', '.join(record.product_tag_ids.mapped('name'))


class im_inventory_rep_pivot(models.Model):
    _inherit = 'product.product'

    im_product_tag = fields.Char(compute='_get_prod_tag', store=True)
    im_avg_cost = fields.Float(compute='_get_other_avg', store=True)
    im_qty = fields.Float(compute='_get_other_qty', store=True)
    im_total_val = fields.Float(compute='_get_other_total_val', store=True)

    @api.depends('product_tmpl_id.im_product_tag_p')
    def _get_prod_tag(self):
        for record in self:
            record.im_product_tag = record.product_tmpl_id.im_product_tag_p

    @api.depends('standard_price')
    def _get_other_avg(self):
        for record in self:
            record.im_avg_cost = record.standard_price

    @api.depends('qty_available')
    def _get_other_qty(self):
        for record in self:
            record.im_qty = record.qty_available

    @api.depends('qty_available', 'standard_price')
    def _get_other_total_val(self):
        for record in self:
            record.im_total_val = record.qty_available * record.standard_price
