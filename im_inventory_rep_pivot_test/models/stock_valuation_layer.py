# -*- coding: utf-8 -*-

from odoo import models, fields, api


class im_inventory_stock_valuation_layer(models.Model):
    _inherit = 'stock.valuation.layer'

    im_product_tag_p = fields.Char(compute='_get_prod_tag_p', store=True)
    # im_avg_cost = fields.Float(string='Avg Cost', compute='_get_product_avg_cost', store=True)

    @api.depends('product_id')
    def _get_prod_tag_p(self):
        for record in self:
            record.im_product_tag_p = record.product_id.im_product_tag_p

    # @api.depends('product_id', 'quantity', 'value')
    # def _get_product_avg_cost(self):
    #     self._cr.execute('''select
    #     product_id,
    #     sum(quantity) as sum_qty,
    #     sum(value) as sum_value
    #     from stock_valuation_layer
    #     group by product_id''')
    #
    #     data = self._cr.dictfetchall()
    #     sum_qty = 0
    #     sum_val = 0
    #     avg_val = 0
    #     for d in data:
    #         if d.get('product_id') == self.product_id.id:
    #             sum_qty = d.get('sum_qty')
    #             sum_val = d.get('sum_value')
    #             avg_val = sum_val/sum_qty if sum_val and sum_qty is not 0 else 0
    #             print('\n',sum_qty,sum_val,avg_val,'\n')
    #             self.im_avg_cost = avg_val
    #         else:
    #             pass

        # self.im_avg_cost = 0
        # print('--' * 30)
        # print(qty_sum, value_sum)
        # print('--' * 30)
