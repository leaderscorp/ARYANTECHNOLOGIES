# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _check_update_qty_permission(self):
        """ Check if current user has permission to update product on-hand quantity """
        user = self.env.user
        if self.env.is_superuser():
            return
        
        # Check both direct boolean field and security group
        if not user.allow_update_qty and not user.has_group('user_qty_update_access.group_allow_update_qty'):
            raise UserError(_("You do not have permission to update product on-hand quantity. Please contact your System Administrator."))

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.is_superuser():
            for vals in vals_list:
                if any(k in vals for k in ('inventory_quantity', 'inventory_quantity_auto_apply', 'inventory_diff_quantity')):
                    self._check_update_qty_permission()
        return super().create(vals_list)

    def write(self, vals):
        if not self.env.is_superuser():
            if any(k in vals for k in ('inventory_quantity', 'inventory_quantity_auto_apply', 'inventory_diff_quantity', 'inventory_quantity_set')):
                self._check_update_qty_permission()
        return super().write(vals)

    def _set_inventory_quantity(self):
        if not self.env.is_superuser():
            self._check_update_qty_permission()
        return super()._set_inventory_quantity()

    def action_apply_inventory(self):
        self._check_update_qty_permission()
        return super().action_apply_inventory()

    def action_set_inventory_quantity(self):
        self._check_update_qty_permission()
        return super().action_set_inventory_quantity()

    def action_set_inventory_quantity_zero(self):
        self._check_update_qty_permission()
        return super().action_set_inventory_quantity_zero()

    def action_clear_inventory_quantity(self):
        self._check_update_qty_permission()
        return super().action_clear_inventory_quantity()
