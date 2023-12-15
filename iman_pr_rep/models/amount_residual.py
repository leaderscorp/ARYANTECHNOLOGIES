from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'



    inv_id_ref = fields.Char(string='Invoice Amount Due', compute='_compute_inv_ref_id')

    bill_id_ref = fields.Char(string='Bill Amount Due', compute='_compute_bill_ref_id')

    bill_balance = fields.Float()
    inv_balance = fields.Float()

    inv_balance_ref_total=fields.Float(compute='_compute_inv_balance_total')
    bill_balance_ref_total=fields.Float(compute='_compute_bill_balance_total')


    # @api.depends('reconciled_invoice_ids')
    # def _compute_inv_ref_id(self):
    #     for rec in self:
    #         for x in rec.reconciled_invoice_ids:
    #             rec.inv_id_ref = x.name
    #
    #
    #
    # @api.depends('reconciled_bill_ids')
    # def _compute_bill_ref_id(self):
    #     for rec in self:
    #         for y in rec.reconciled_bill_ids:
    #             rec.bill_id_ref = y.name

    @api.depends('reconciled_invoice_ids')
    def _compute_inv_ref_id(self):
        for rec in self:
            rec.inv_id_ref = ' '.join([x.name for x in rec.reconciled_invoice_ids])



    @api.depends('reconciled_bill_ids')
    def _compute_bill_ref_id(self):
        for rec in self:
            rec.bill_id_ref = ' '.join([x.name for x in rec.reconciled_bill_ids])

    # @api.depends('reconciled_invoice_ids')
    # def _compute_inv_balance(self):
    #     for payment in self:
    #         for data in payment.reconciled_invoice_ids:
    #             payment.inv_balance = data.amount_residual
    #
    # @api.depends('reconciled_bill_ids')
    # def _compute_bill_balance(self):
    #     for payment in self:
    #         for data in payment.reconciled_bill_ids:
    #             payment.bill_balance = data.amount_residual

    @api.depends('reconciled_invoice_ids')
    def _compute_inv_balance_total(self):
        for payment in self:
            x=0
            for data in payment.reconciled_invoice_ids:
                x = x + data.amount_total
                payment.inv_balance_ref_total = x



    @api.depends('reconciled_bill_ids')
    def _compute_bill_balance_total(self):

        for payment in self:
            x = 0
            for data in payment.reconciled_bill_ids:
                x = x + data.amount_total
                payment.bill_balance_ref_total = x



    # print(inv_amount_due)