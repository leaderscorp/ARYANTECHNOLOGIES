# -*- coding: utf-8 -*-

from lxml import etree
from odoo import models, fields, api

# PRODUCTION_UID = 11
# REQUESTION_PICKING_TYPE_ID = 42

class im_mo_requestion(models.Model):
    _inherit = 'stock.picking'

    hide_button = fields.Boolean(
        string='Hide_Button',
        required=False,
        default=False
    )

    env_user = fields.Integer(
        compute='_onchange_user'
    )

    mo_num = fields.Char(
        string='MO No'
    )

    so_num = fields.Char(
        string='SO No'
    )

    def _onchange_user(self):
        for rec in self:
            rec.env_user = rec.env.user.id
            # print(rec.env_user)


    # @api.model
    # def get_view(self, view_id=None, view_type='form', **options):
    #     res = super(im_mo_requestion, self).get_view(view_id, view_type, **options)
    #     if view_type == 'form':
    #
    #         model = str(res['model'])
    #         active_id = None
    #         if self._context.get('params') and self._context.get('params').get('model') == 'stock.picking':
    #             active_id = self._context.get('params').get('id')
    #         elif self._context.get('stock_picking_id'):
    #             active_id = self._context.get('stock_picking_id')
    #         else:
    #             print('Error or else case')
    #             pass
    #         record = self.env[model].browse(active_id)
    #         uid = self.env.user.id
    #
    #         doc = etree.XML(res['arch'])
    #         action_confirm = doc.xpath("//button[@name='action_confirm']")
    #         print(self._context)
    #         print(res['arch'])
            # print(record.picking_type_id.id)
            # uid = user_id of production user (11)
            # picking_type_id = requestion operation type (42)
            # if action_confirm and uid == PRODUCTION_UID and record.picking_type_id.id == REQUESTION_PICKING_TYPE_ID:
            #     print(action_confirm[0].attrib.items())
                # action_confirm[0].set('modifiers', '{"invisible": true}')
                # action_confirm[0].set('invisible', '1')
            # else:
            #     pass
            # res['arch'] = etree.tostring(doc, encoding='unicode')
        # return res