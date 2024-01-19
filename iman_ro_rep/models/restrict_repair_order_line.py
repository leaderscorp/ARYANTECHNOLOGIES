from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class IMRepairOrderRestrict(models.Model):
    _inherit = 'repair.order'
    newfield=fields.Char(string='test')
    def action_validate(self):
        for order in self:
            products_with_insufficient_quantity = [
                line.product_id.display_name  # Get the product's display name
                for line in order.operations
                if line.product_id.qty_available <= 0
            ]
            if products_with_insufficient_quantity:
                raise UserError(
                    _('You cannot confirm this repair order. The following products have insufficient quantity: %s') %
                    ', '.join(products_with_insufficient_quantity)
                )
            else:
                super(IMRepairOrderRestrict, order).action_validate()