from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
        for order in self:
            repair = self.env['repair.order'].search([
                ('sale_order_id', '=', order.id)
            ], limit=1)

            order.repair_number = repair.seq_desc if repair else False

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoices = super()._create_invoices(grouped, final, date)

        for inv in invoices:
            inv.description_text = self.description_text
            inv.site_location = self.site_location


        return invoices        