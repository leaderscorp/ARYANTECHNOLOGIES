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
    _inherit = 'account.move.line'

    im_product_tag = fields.Char(compute='_get_prod_tag', store=True)

    @api.depends('product_id.im_product_tag_p')
    def _get_prod_tag(self):
        for record in self:
            record.im_product_tag = record.product_id.im_product_tag_p
