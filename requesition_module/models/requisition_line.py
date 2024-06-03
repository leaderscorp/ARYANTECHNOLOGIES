from odoo import models, fields, api, _

class Requisition(models.Model):
    _name = 'requisition.line'  # Use 'request' instead of 'requesition' for Odoo convention
    _description = 'Requisition Module'

    # name = fields.Char(string="Product Name")
    req_id = fields.Many2one('request.model',string="Requisition Id")
    product_id  = fields.Many2one("product.product")
    location_id  = fields.Many2one("stock.location")
    location_dest_id  = fields.Many2one("stock.location")
    product_uom_quantity = fields.Char(string="Quantity")
