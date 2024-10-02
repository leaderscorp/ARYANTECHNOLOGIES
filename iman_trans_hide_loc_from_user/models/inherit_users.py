from odoo import models, fields, api


class Inheritsers(models.Model):
    _inherit = 'res.users'

    location_ids = fields.Many2many(
        comodel_name='stock.location',
        relation='rel_locs',
        help='Specify the locations this user can use'
    )

    dest_location_ids = fields.Many2many(
        comodel_name='stock.location',
        relation='rel_dest_locs',
        help='Specify the Destination locations this user can use'
    )

    picking_type_ids = fields.Many2many(
        comodel_name='stock.picking.type',
        help='Specify the operation this user can use'
    )