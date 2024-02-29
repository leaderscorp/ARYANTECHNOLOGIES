from odoo import models, fields, api


class InheritPO(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('user_id')
    def onchange_user(self):
        for rec in self:
            if rec.user_id.id == 9:
                return {
                    'domain': {
                        'picking_type_id': [
                            # ('warehouse_id', 'like', 'After Sales Warehouse'),
                            ('warehouse_id', '=', 2),
                            ('code', '=', 'incoming'),
                            '|',
                            ('warehouse_id', '=', False),
                            ('warehouse_id.company_id.id', '=', rec.company_id.id)]
                    }
                }
            elif rec.user_id.id == 10:
                return {
                    'domain': {
                        'picking_type_id': [
                            ('warehouse_id', '=', 1),
                            ('code', '=', 'incoming'),
                            '|',
                            ('warehouse_id', '=', False),
                            ('warehouse_id.company_id.id', '=', rec.company_id.id)
                            ]
                    }
                }
            else:
                return {
                    'domain': {
                        'picking_type_id': [
                            ('code', '=', 'incoming'),
                            '|',
                            ('warehouse_id', '=', False),
                            ('warehouse_id.company_id.id', '=', rec.company_id.id)
                        ]
                    }
                }