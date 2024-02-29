from odoo import models, fields, api


# class InheritRepairOrder(models.Model):
    # _inherit = 'repair.order'

    # _inherit = 'repair.line'
    #
    # @api.onchange('repair_id.user_id')
    # def _onchange_user_id_for_location(self):
    #     for line in self:
    #         if line.repair_id.user_id.id == 9:
    #             # Domain to restrict both location_id and location_dest_id based on the complete_name
    #             domain = {
    #                 'location_id': [('complete_name', 'like', 'ASW')],
    #                 'location_dest_id': [('complete_name', 'like', 'ASW')]
    #             }
    #             # Optionally, you can set a specific location that matches this criteria as default
    #             # This would require querying for locations that match the domain criteria
    #             # Example for setting a default location (assuming only one matches the criteria):
    #             location = self.env['stock.location'].search([('complete_name', 'like', 'ASW')], limit=1)
    #             if location:
    #                 line.location_id = location.id
    #                 line.location_dest_id = location.id
    #             return {'domain': domain}
    #         else:
    #             # For users other than user_id 9, you can adjust this as needed
    #             # This example clears the domain restrictions for these fields
    #             return {'domain': {'location_id': [], 'location_dest_id': []}}

    # @api.onchange('operations')
    # def onchange_user(self):
    #     for rec in self:
    #         print('ok')
    #         if rec.user_id.id == 9:
    #             return {'domain': {
    #                 'location_id': [('complete_name', 'like', 'WH')]
                    # 'location_dest_id': [('complete_name', 'like', 'ASW')],
                # }
            # }
                    # return {
                    #     'domain': {
                    #         'location_id': [('complete_name', 'like', 'ASW')],
                    #         'location_dest_id': [('complete_name', 'like', 'ASW')],
                    #     }
                    # }
            # elif rec.user_id.id == 10:
            #     return {
            #         'domain': {
            #             'location_id': [('complete_name', 'in', ['WH',
            #                                                      'WH/Islamabad',
            #                                                      'ASW/Islamabad',
            #                                                      'Prod/Stock',
            #                                                      'WH/Islamabad/CMC MACHINE (C/O AHMED SAB)',
            #                                                      'WH/Islamabad/LUCKY MACHINERY',
            #                                                      'WH/Islamabad/Tarnol Warehouse',
            #                                                      'WH/Islamabad/Tarnol Warehouse (Finish goods)'])],
            #             'location_dest_id': [('complete_name', 'in', ['WH',
            #                                                           'WH/Islamabad',
            #                                                           'ASW/Islamabad',
            #                                                           'Prod/Stock',
            #                                                           'WH/Islamabad/CMC MACHINE (C/O AHMED SAB)',
            #                                                           'WH/Islamabad/LUCKY MACHINERY',
            #                                                           'WH/Islamabad/Tarnol Warehouse',
            #                                                           'WH/Islamabad/Tarnol Warehouse (Finish goods)'])],
            #         }
            #     }
            # else:
            #     return {
            #         'domain': {
            #             'location_id': [],
            #             'location_dest_id': [],
            #         }
            #     }