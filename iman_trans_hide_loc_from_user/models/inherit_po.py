from odoo import models, fields, api


class InheritPO(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('user_id')
    def onchange_user(self):
        picking_type_ids = self.env.user.picking_type_ids.mapped('id')
        domain = {}
        if picking_type_ids != []:
            domain.update({
                'picking_type_id': [('id', 'in', picking_type_ids),
                                    ('code', '=', 'incoming'),
                                    '|',
                                    ('warehouse_id', '=', False),
                                    ('warehouse_id.company_id.id', '=', self.env.company.id)
                                    ]
            })
        else:
            domain.update({'picking_type_id': [
                            ('code', '=', 'incoming'),
                            '|',
                            ('warehouse_id', '=', False),
                            ('warehouse_id.company_id.id', '=', self.env.company.id)
                        ]})
        return {'domain': domain}

        # for rec in self:
        #     if rec.user_id.id == 9:
        #         return {
        #             'domain': {
        #                 'picking_type_id': [
        #                     ('warehouse_id', '=', 2),
        #                     ('code', '=', 'incoming'),
        #                     '|',
        #                     ('warehouse_id', '=', False),
        #                     ('warehouse_id.company_id.id', '=', rec.company_id.id)]
        #             }
        #         }
        #     elif rec.user_id.id == 10:
        #         return {
        #             'domain': {
        #                 'picking_type_id': [
        #                     ('warehouse_id', '=', 1),
        #                     ('code', '=', 'incoming'),
        #                     '|',
        #                     ('warehouse_id', '=', False),
        #                     ('warehouse_id.company_id.id', '=', rec.company_id.id)
        #                     ]
        #             }
        #         }
        #     else:
        #         return {
        #             'domain': {
        #                 'picking_type_id': [
        #                     ('code', '=', 'incoming'),
        #                     '|',
        #                     ('warehouse_id', '=', False),
        #                     ('warehouse_id.company_id.id', '=', rec.company_id.id)
        #                 ]
        #             }
        #         }