from odoo import models, fields, api


class InheritRepairOrder(models.Model):
    _inherit = 'repair.order'

    loc_ids = fields.Many2many(
        related="user_id.location_ids"
    )

