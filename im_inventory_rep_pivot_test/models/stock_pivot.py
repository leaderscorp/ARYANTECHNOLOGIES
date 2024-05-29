# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools


class im_wip_rep(models.Model):
    _name = 'im_stock.report'
    _description = 'im_stock.report'
    _auto = False


    product_id = fields.Many2one('product.product')
    im_product_tag = fields.Char()
    im_qty = fields.Float()
    reference = fields.Char()
    im_product_cost = fields.Float()
    im_total_cost = fields.Float()


    def init(self):
        tools.drop_view_if_exists(self._cr, 'im_stock_report')
        self._cr.execute(
            """
            CREATE OR REPLACE VIEW im_wip AS (
            select 
            svl.product_id as product_id,
            pp.im_product_tag as im_product_tag,
            pp.im_qty as im_qty,
            sum(svl.quantity) as quantity,
            sum(svl.value) as value,
            (sum(svl.value)/NULLIF(sum(svl.quantity),0)) as avg_cost,
            (pp.im_qty * (sum(svl.value)/NULLIF(sum(svl.quantity),0))) as total_val
            from stock_valuation_layer svl
            join product_product pp on pp.id = svl.product_id
            group by
            svl.product_id,
            pp.im_qty,
            pp.im_product_tag,
            )
            """
        )

