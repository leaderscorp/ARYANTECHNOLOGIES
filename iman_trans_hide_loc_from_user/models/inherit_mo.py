from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    remaining_quantity = fields.Float(
        string='Remaining Quantity',
        default=0.0,
    )