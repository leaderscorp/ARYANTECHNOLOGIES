# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools


class im_wip_rep(models.Model):
    _name = 'im.wip'
    _description = 'im.wip'
    _auto = False


    reference = fields.Char()
    product_uom_qty = fields.Float()
    im_product_cost = fields.Float()
    product_id = fields.Many2one('product.product')
    im_product_tag_p = fields.Char()


    def init(self):
        tools.drop_view_if_exists(self._cr, 'im_wip')
        self._cr.execute(
            """
            CREATE OR REPLACE VIEW im_wip AS (
            select 
            id, 
            reference as reference, 
            product_uom_qty as product_uom_qty, 
            product_id as product_id, 
            im_product_tag_p as im_product_tag_p,
            im_product_cost as im_product_cost,
            COALESCE(production_id, raw_material_production_id) as productions
            from stock_move 
            where im_mrp_state='draft' 
            and company_id=1 
            and COALESCE(production_id, raw_material_production_id) is not null
            )
            """
        )

