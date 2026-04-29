from odoo import models, fields, api


class InheritRepairOrder(models.Model):
    _inherit = 'repair.order'

    loc_ids = fields.Many2many(
    'stock.location',
    compute='_compute_loc_ids',
    string='Locations',
)

    @api.depends('user_id', 'company_id')
    def _compute_loc_ids(self):
        for record in self:
            if record.user_id and record.company_id:
                # Filter user's locations that belong to the current company
                record.loc_ids = record.user_id.location_ids.filtered(
                    lambda l: l.company_id == record.company_id
                )
            else:
                record.loc_ids = record.user_id.location_ids

