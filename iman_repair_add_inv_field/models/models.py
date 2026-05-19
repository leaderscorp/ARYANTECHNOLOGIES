# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words

class AccountPaymentsNumWords(models.Model):
    _inherit='repair.order'
    
    invoice_id = fields.Many2one('account.move')

    inv_name = fields.Char(string="Invoice Name", copy=False)
    inv_date = fields.Date(string='Invoice Date', copy=False)


    quotation_notes = fields.Html('Quotation Notes')

    @api.onchange('invoice_id')
    def _onchange_invoice_id(self):
        for repair in self:
            if repair.invoice_id:
                repair.inv_name = repair.invoice_id.name
                repair.inv_date = repair.invoice_id.invoice_date
    # fees_lines = fields.One2many(
    #     'repair.fee', 'repair_id', 'Operations',
    #     copy=True, readonly=False)
    
    # currency_id = fields.Many2one(related='pricelist_id.currency_id')
    # pricelist_id = fields.Many2one(
    #     'product.pricelist', 'Pricelist',
    #     default=lambda self: self.env['product.pricelist'].search([('company_id', 'in', [self.env.company.id, False])], limit=1).id,
    #     help='Pricelist of the selected partner.', check_company=True)
    


    # amount_untaxed = fields.Float('Untaxed Amount', compute='_amount_untaxed', store=True)
    # amount_tax = fields.Float('Taxes', compute='_amount_tax', store=True)
    # amount_total = fields.Float('Total', compute='_amount_total', store=True)




    # @api.depends('move_ids.price_unit', 'move_ids.quantity', 'invoice_method', 'fees_lines.price_subtotal', 'pricelist_id.currency_id')
    # def _amount_untaxed(self):
    #     for order in self:
    #         total = sum(move.price_unit * move.quantity for move in order.move_ids)
    #         total += sum(fee.price_subtotal for fee in order.fees_lines)
    #         currency = order.pricelist_id.currency_id or self.env.company.currency_id
    #         order.amount_untaxed = currency.round(total)

    # @api.depends('move_ids.price_unit', 'move_ids.quantity', 'move_ids.product_id',
    #              'fees_lines.price_unit', 'fees_lines.product_uom_qty', 'fees_lines.product_id',
    #              'pricelist_id.currency_id', 'partner_id')
    # def _amount_tax(self):
    #     for order in self:
    #         val = 0.0
    #         currency = order.pricelist_id.currency_id or self.env.company.currency_id
    #         for operation in order.move_ids:
    #             if operation.tax_id:
    #                 tax_calculate = operation.tax_id.compute_all(operation.price_unit, currency, operation.quantity, operation.product_id, order.partner_id)
    #                 for c in tax_calculate['taxes']:
    #                     val += c['amount']
    #         for fee in order.fees_lines:
    #             if fee.tax_id:
    #                 tax_calculate = fee.tax_id.compute_all(fee.price_unit, currency, fee.product_uom_qty, fee.product_id, order.partner_id)
    #                 for c in tax_calculate['taxes']:
    #                     val += c['amount']
    #         order.amount_tax = val

    # @api.depends('amount_untaxed', 'amount_tax')
    # def _amount_total(self):
    #     for order in self:
    #         currency = order.pricelist_id.currency_id or self.env.company.currency_id
    #         order.amount_total = currency.round(order.amount_untaxed + order.amount_tax)


