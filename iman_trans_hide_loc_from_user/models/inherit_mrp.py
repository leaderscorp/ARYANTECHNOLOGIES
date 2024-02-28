from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.onchange('move_raw_ids')
    # @api.depends('move_raw_ids.quantity_done')
    def _call_meth_on_state(self):
        if self.state in ['progress', 'to_close', 'done']:
            self._compute_remaining_quantity()
        else:
            pass
    def _compute_remaining_quantity(self):
        for record in self:
            for move in record.move_raw_ids:
                if move.forecast_availability > 0:
                    move.remaining_quantity = move.forecast_availability - move.quantity_done
                # elif move.product_uom_quantity > 0:
                #     move.remaining_quantity = move.product_uom_quantity - move.quantity_done
                else:
                    move.remaining_quantity = 0.0
