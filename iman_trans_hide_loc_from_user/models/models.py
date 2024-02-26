from odoo import models, fields, api



class iman_trans_hide_loc_from_user(models.Model):

    _inherit = 'stock.picking'

    @api.onchange('user_id')
    def onchange_user(self):
        for rec in self:
            if rec.user_id.id == 9:
                return {
                    'domain': {
                        'location_id': [('complete_name', 'like', 'ASW')],
                        'location_dest_id': [('complete_name', 'like', 'ASW')]
                    }
                }
            elif rec.user_id.id == 10:
                return {
                    'domain': {
                        'location_id': [('complete_name', 'in', ['WH', 'WH/Islamabad', 'ASW/Islamabad'])],
                        'location_dest_id': [('complete_name', 'in', ['WH', 'WH/Islamabad', 'ASW/Islamabad'])]
                    }
                }
            else:
                pass