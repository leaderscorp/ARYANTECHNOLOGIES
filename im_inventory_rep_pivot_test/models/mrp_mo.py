# -*- coding: utf-8 -*-

from odoo import models, fields, api


class im_mo_mrp(models.Model):
    _inherit = 'mrp.production'


    env_user = fields.Integer(
        compute='_onchange_user'
    )

    so_num = fields.Char(
        string='SO Num'
    )

    def _onchange_user(self):
        for rec in self:
            rec.env_user = rec.env.user.id

