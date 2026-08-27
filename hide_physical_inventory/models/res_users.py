from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    hide_physical_inventory = fields.Boolean(
        string="Hide Physical Inventory Menu",
        default=False,
        help="Check this box to hide the Physical Inventory menu for this user."
    )

    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        if 'hide_physical_inventory' in vals:
            self.env.registry.clear_cache()
        return res
