from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    repair_number = fields.Char(
        string="Repair Number",
        compute="_compute_repair_number",
    )

    description_text = fields.Char(
        string="Description",
        index=True
    )

    site_location = fields.Char(
        string="Site Location",
    )

    def _compute_repair_number(self):
        for move in self:
            sale = self.env['sale.order'].search([
                ('name', '=', move.invoice_origin)
            ], limit=1)

            repair = self.env['repair.order'].search([
                ('sale_order_id', '=', sale.id)
            ], limit=1) if sale else False

            move.repair_number = repair.seq_desc if repair else False