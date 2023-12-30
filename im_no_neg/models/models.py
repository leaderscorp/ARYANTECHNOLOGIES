# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class repair(models.Model):
    _inherit = 'repair.order'

    def action_validate(self):
        for product in self.operations:
            if product.product_id.qty_available < product.product_uom_qty:
                raise UserError("Product: %s has low quantity than requested quantity" %(product.product_id.name))

        return super(repair, self).action_validate()
