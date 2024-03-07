# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class repair(models.Model):
    _inherit = 'repair.order'

    def action_validate(self):
        # for product in self.operations:
        #     if product.product_id.qty_available < product.product_uom_qty:
        #         raise UserError("Product: %s has low quantity than requested quantity" %(product.product_id.name))

        # for rec in self:
            for comp in self.operations:
                prod_in_comp = self.env['stock.quant'].search([
                    ('on_hand', '=', True),
                    ('product_id', '=', comp.product_id.id),
                    ('product_id.detailed_type', '=', 'product'),
                    ('location_id', '=', comp.location_id.id)
                    ])

                if prod_in_comp and comp.product_id.detailed_type == 'product':
                    if 0 < prod_in_comp.quantity < comp.product_uom_qty:
                        message = f"Product: {comp.product_id.name} has low quantity than requested quantity in {comp.location_id.display_name}"
                        raise UserError(message)

                elif not prod_in_comp and comp.product_id.detailed_type == 'product':
                    message = f"The location {comp.location_id.display_name} does not have the product {comp.product_id.name}"
                    raise UserError(message)
                else:
                    pass

            return super(repair, self).action_validate()
