from odoo import models, fields

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    description_text = fields.Char(
        string="Description",
        index=True
    )

    site_location = fields.Char(
        string="Site Location",
    )

    def action_create_sale_order(self):
        res = super().action_create_sale_order()

        sale_order = self.sale_order_id
        if sale_order:
            sale_order.description_text = self.description_text
            sale_order.site_location = self.site_location

        return res