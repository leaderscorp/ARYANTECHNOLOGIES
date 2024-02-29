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
                        'location_dest_id': [('complete_name', 'like', 'ASW')],
                        'picking_type_id': [('warehouse_id', 'like', 'After Sales Warehouse')]
                    }
                }
            elif rec.user_id.id == 10:
                return {
                    'domain': {
                        'location_id': [('complete_name', 'in', ['WH',
                                                                 'WH/Islamabad',
                                                                 'ASW/Islamabad',
                                                                 'Prod/Stock',
                                                                 'WH/Islamabad/CMC MACHINE (C/O AHMED SAB)',
                                                                 'WH/Islamabad/LUCKY MACHINERY',
                                                                 'WH/Islamabad/Tarnol Warehouse',
                                                                 'WH/Islamabad/Tarnol Warehouse (Finish goods)'])],
                        'location_dest_id': [('complete_name', 'in', ['WH',
                                                                      'WH/Islamabad',
                                                                      'ASW/Islamabad',
                                                                      'Prod/Stock',
                                                                      'WH/Islamabad/CMC MACHINE (C/O AHMED SAB)',
                                                                      'WH/Islamabad/LUCKY MACHINERY',
                                                                      'WH/Islamabad/Tarnol Warehouse',
                                                                      'WH/Islamabad/Tarnol Warehouse (Finish goods)'])],
                        'picking_type_id': [('warehouse_id', 'like', 'Islamabad WH')]
                    }
                }
            else:
                return {
                    'domain': {
                        'location_id': [],
                        'location_dest_id': [],
                        'picking_type_id': []
                    }
                }