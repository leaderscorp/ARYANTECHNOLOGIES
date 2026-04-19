from odoo import models, fields, api, _


class Requisition(models.Model):
    _name = 'requisition.line'  # Use 'request' instead of 'requesition' for Odoo convention
    _description = 'requisition.line'

    req_id = fields.Many2one(
        comodel_name='request.model',
        string="Requisition Id",
        ondelete='cascade',
    )
    product_id = fields.Many2one(comodel_name="product.product")
    location_id = fields.Many2one(comodel_name="stock.location")
    location_dest_id = fields.Many2one(comodel_name="stock.location")
    product_uom_quantity = fields.Char(string="Quantity")
