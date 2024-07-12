# -*- coding: utf-8 -*-

from odoo import models, fields, api


class im_inventory_product(models.Model):
    _inherit = 'product.template'

    im_product_tag_p = fields.Char(compute='_get_prod_tag_p')
    # im_prod_avg_cost = fields.Float(compute='_get_prod_avg_cost')
    #
    # def get_avg_cost(self, id):
    #     self._cr.execute(f'''select
    #                      product_id,
    #                      sum(quantity) as sum_qty,
    #                      sum(value) as sum_value
    #                      from stock_valuation_layer
    #                      where product_id = %s
    #                      ''', [id])
    #     query_data = self._cr.dictfetchall()
    #     print(query_data)
    #     sum_qty, sum_value, avg_cost = 0, 0, 0
    #     if query_data:
    #         sum_qty = query_data.get('sum_qty')
    #         sum_value = query_data.get('sum_value')
    #         avg_cost = 0
    #     if sum_qty != 0 and sum_value != 0:
    #         avg_cost = sum_value/sum_qty
    #     else:
    #         pass
    #     return avg_cost

    # @api.depends('qty_available')
    # def _get_prod_avg_cost(self):
    #     self.im_prod_avg_cost = self.get_avg_cost(id=self.id)

    @api.depends('product_tag_ids.name')
    def _get_prod_tag_p(self):
        for record in self:
            record.im_product_tag_p = ', '.join(record.product_tag_ids.mapped('name'))




class im_inventory_rep_pivot(models.Model):
    _inherit = 'product.product'

    im_product_tag = fields.Char(compute='_get_prod_tag', store=True)
    im_product_cost = fields.Float(compute='_get_prod_cost', store=True)
    im_qty = fields.Float(compute='_get_other_qty', store=True)
    im_total_val = fields.Float(compute='_get_other_total_val', store=True)

    @api.depends('product_tmpl_id.im_product_tag_p')
    def _get_prod_tag(self):
        for record in self:
            record.im_product_tag = record.product_tmpl_id.im_product_tag_p


    @api.depends('standard_price')
    def _get_prod_cost(self):
        for record in self:
            record.im_product_cost = record.standard_price

    @api.depends('qty_available')
    def _get_other_qty(self):
        for record in self:
            record.im_qty = record.qty_available

    @api.depends('qty_available', 'standard_price')
    def _get_other_total_val(self):
        for record in self:
            record.im_total_val = record.qty_available * record.standard_price
