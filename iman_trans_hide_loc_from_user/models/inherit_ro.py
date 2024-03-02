from odoo import models, fields, api


class InheritRepairOrder(models.Model):
    _inherit = 'repair.line'

    @api.onchange(
        'type',
        'location_id',
        'location_dest_id'
    )
    def _onchange_user_id_for_location(self):
        data = self.env.user.location_ids.mapped('id')
        if data == []:
            domain = []
        else:
            domain = {
                'location_id': [('id', 'in', data)],
                'location_dest_id': [('id', 'in', data)]
            }
        return {'domain': domain}
