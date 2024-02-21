from odoo import models,fields,api
from num2words import num2words

class AccountRepairOrderNumWords(models.Model):
    _inherit = 'repair.order'

    job_completion_date = fields.Date(string = "Job Completion Date")

    invoice_method2 = fields.Selection([
        ("b4repair", "Before Repair"),
        ("after_repair", "After Repair")],
        string="Invoice Method",
        default='after_repair',
        index=True,
        required=True,
        states={'draft': [('readonly', False)]},
        help='Selecting \'Before Repair\' or \'After Repair\' will allow you to generate invoice before or after the repair is done respectively. \'No invoice\' means you don\'t want to generate invoice for this repair order.')


    @api.onchange('invoice_method2')
    def _onchange_invoice_method2(self):
        self.invoice_method = self.invoice_method2

    check_tax = fields.Float(
        string='tax amt',
        compute='get_tax',
        required=False,
        store=True)

    tax_id_num = fields.Char(
        compute='cal_tax_val'
    )

    total_in_wordss = fields.Char(compute='int_to_words')
    # @api.depends('tax_ids')
    def cal_tax_val(self):
        for rec in self:
            pass
    #         rec.tax_id_num = ', '.join([(str(x.amount) + ' %') for x in rec.tax_ids])


    # dummy = fields.Char(default="Dummy Text",string="dummy")
    @api.depends('amount_total')
    def int_to_words(self):
        for rec in self:
            rec.total_in_wordss = num2words(rec.amount_total, lang='en_US')


    @api.depends('operations.tax_id.amount')
    def get_tax(self):
        for parts_tax in self.mapped('operations.tax_id'):
            print(parts_tax.amount)
            # for tax in item.tax_id:
            #     pass
                # tax_amount = (item.price_subtotal * tax.amount) / 100
                # print(tax_amount)
                # total_tax = tax_amount
                # print(total_tax)
                # item.check_tax = total_tax
