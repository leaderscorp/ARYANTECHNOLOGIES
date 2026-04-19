# -*- coding: utf-8 -*-

from odoo import models, fields, api


class im_inventory_stock_move(models.Model):
    _inherit = 'stock.move'

    im_product_tag_p = fields.Char(compute='_get_prod_tag_p', store=True)
    im_mrp_state = fields.Char(compute='_get_mrp', store=True)
    im_product_cost = fields.Float(compute='_get_prod_cost', store=True)

    @api.depends('product_id.standard_price')
    def _get_prod_cost(self):
        for record in self:
            record.im_product_cost = record.product_id.standard_price

    @api.depends('product_id.im_product_tag_p')
    def _get_prod_tag_p(self):
        for record in self:
            record.im_product_tag_p = record.product_id.im_product_tag_p

    @api.depends('production_id.state', 'raw_material_production_id.state')
    def _get_mrp(self):
        for record in self:
            if record.production_id:
                record.im_mrp_state = record.production_id.state
            elif record.raw_material_production_id:
                record.im_mrp_state = record.raw_material_production_id.state
