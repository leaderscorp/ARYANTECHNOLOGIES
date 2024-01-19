from odoo import models, fields, api, _
# from odoo.exceptions import UserError, ValidationError


class IMRepairLocationRestrict(models.Model):
    _inherit = 'repair.line'

    location_id = fields.Many2one(
        'stock.location', 'Location',
        domain="[('complete_name' ',!=' , 'WH/Islamabad')]",
        compute="_compute_location_id", store=True, precompute=True,
        index=True, readonly=True, required=True, check_company=True,
        help="This is the location where the product to repair is located.",
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', True)]})

