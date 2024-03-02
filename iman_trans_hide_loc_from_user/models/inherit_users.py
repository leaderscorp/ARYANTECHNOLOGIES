from odoo import models, fields, api


class Inheritsers(models.Model):
    _inherit = 'res.users'

    location_ids = fields.Many2many(
        comodel_name='stock.location',
        help='Specify the locations this user can use'
    )

    picking_type_ids = fields.Many2many(
        comodel_name='stock.picking.type',
        help='Specify the operation this user can use'
    )