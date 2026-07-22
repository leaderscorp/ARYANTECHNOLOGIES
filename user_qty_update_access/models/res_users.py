# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.fields import Command

class ResUsers(models.Model):
    _inherit = 'res.users'

    allow_update_qty = fields.Boolean(
        string="Allow Update Product On-Hand Quantity",
        compute='_compute_allow_update_qty',
        inverse='_inverse_allow_update_qty',
        store=True,
        help="If checked, this user is allowed to update product on-hand quantity.",
    )

    @api.depends('group_ids')
    def _compute_allow_update_qty(self):
        group = self.env.ref('user_qty_update_access.group_allow_update_qty', raise_if_not_found=False)
        for user in self:
            if group and group in user.group_ids:
                user.allow_update_qty = True
            else:
                user.allow_update_qty = False

    def _inverse_allow_update_qty(self):
        group = self.env.ref('user_qty_update_access.group_allow_update_qty', raise_if_not_found=False)
        if not group:
            return
        for user in self:
            if user.allow_update_qty:
                if group not in user.group_ids:
                    user.sudo().write({'group_ids': [Command.link(group.id)]})
            else:
                if group in user.group_ids:
                    user.sudo().write({'group_ids': [Command.unlink(group.id)]})
