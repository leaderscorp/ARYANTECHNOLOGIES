from odoo import models

class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    def _filter_visible_menus(self):
        menus = super(IrUiMenu, self)._filter_visible_menus()
        if self.env.user.hide_physical_inventory:
            physical_inventory_menu = self.env.ref('stock.menu_action_inventory_tree', raise_if_not_found=False)
            if physical_inventory_menu and physical_inventory_menu in menus:
                menus -= physical_inventory_menu
        return menus
