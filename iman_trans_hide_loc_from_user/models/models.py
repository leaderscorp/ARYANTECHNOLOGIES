from odoo import models, fields, api


class iman_trans_hide_loc_from_user(models.Model):

    _inherit = 'stock.picking'

    loc_ids = fields.Many2many(
        related="user_id.location_ids"
        )
    pick_ids = fields.Many2many(
        related="user_id.picking_type_ids"
    )
    # @api.onchange('user_id')
    # def onchange_user(self):
    #     location_ids = self.env.user.location_ids.mapped('id')
    #     picking_type_ids = self.env.user.picking_type_ids.mapped('id')
    #     domain = {}
    #     if location_ids != [] and picking_type_ids != []:
    #         domain.update({
    #             'location_id': [('id', 'in', location_ids)],
    #             'location_dest_id': [('id', 'in', location_ids)],
    #             'picking_type_id': [('id', 'in', picking_type_ids)],
    #         })
    #     elif location_ids != []:
    #         domain.update({
    #             'location_id': [('id', 'in', location_ids)],
    #             'location_dest_id': [('id', 'in', location_ids)],
    #         })
    #     elif picking_type_ids != []:
    #         domain.update({
    #             'picking_type_id': [('id', 'in', picking_type_ids)]
    #         })
    #
    #     else:
    #         domain.update({
    #             'location_id': [],
    #             'location_dest_id': [],
    #             'picking_type_id': [],
    #         })
    #     return {'domain': domain}

        # for rec in self:
        #     if rec.user_id.id == 9:
        #         return {
        #             'domain': {
        #                 'location_id': [('complete_name', 'like', 'ASW')],
        #                 'location_dest_id': [('complete_name', 'like', 'ASW')],
        #                 'picking_type_id': [('warehouse_id', 'like', 'After Sales Warehouse')]
        #             }
        #         }
        #     elif rec.user_id.id == 10:
        #         return {
        #             'domain': {
        #                 'location_id': [('complete_name', 'in', ['WH',
        #                                                          'WH/Islamabad',
        #                                                          'ASW/Islamabad',
        #                                                          'Prod/Stock',
        #                                                          'WH/Islamabad/CMC MACHINE (C/O AHMED SAB)',
        #                                                          'WH/Islamabad/LUCKY MACHINERY',
        #                                                          'WH/Islamabad/Tarnol Warehouse',
        #                                                          'WH/Islamabad/Tarnol Warehouse (Finish goods)'])],
        #                 'location_dest_id': [('complete_name', 'in', ['WH',
        #                                                               'WH/Islamabad',
        #                                                               'ASW/Islamabad',
        #                                                               'Prod/Stock',
        #                                                               'WH/Islamabad/CMC MACHINE (C/O AHMED SAB)',
        #                                                               'WH/Islamabad/LUCKY MACHINERY',
        #                                                               'WH/Islamabad/Tarnol Warehouse',
        #                                                               'WH/Islamabad/Tarnol Warehouse (Finish goods)'])],
        #                 'picking_type_id': [('warehouse_id', 'like', 'Islamabad WH')]
        #             }
        #         }
        #     else:
        #         return {
        #             'domain': {
        #                 'location_id': [],
        #                 'location_dest_id': [],
        #                 'picking_type_id': []
        #             }
        #         }