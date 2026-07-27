# -*- coding: utf-8 -*-
from odoo import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_print_tax_invoice(self):
        """Action function to trigger PDF print for PRINT TAX INVOICE REPORT"""
        return self.env.ref('custom_tax_invoice.action_report_print_tax_invoice').report_action(self)