from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    remaining_quantity = fields.Float(
         string='Remaining Quantity',
         default=0.0,
        # compute='_compute_remaining_quantity'
    )

    # def _compute_remaining_quantity(self):
    #     for move in self:
    #         if move.raw_material_production_id:
    #             if move.forecast_availability > 0:
    #                 move.remaining_quantity = move.forecast_availability - move.quantity_done
                # elif move.product_uom_quantity > 0:
                #     move.remaining_quantity = move.product_uom_quantity - move.quantity_done
                # else:
                #     move.remaining_quantity = 0.0
