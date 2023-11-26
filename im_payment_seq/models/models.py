from odoo import fields, api, models


class IMAccountRegisterPayment(models.TransientModel):
    _inherit = 'account.payment.register'

    def _create_payment_vals_from_wizard(self, batch_result):
        res = super(IMAccountRegisterPayment, self)._create_payment_vals_from_wizard(batch_result)
        if self.env.user.company_id.id == 1:
            for line in self.line_ids.move_id:
                if line.move_type == 'entry':
                    if self.journal_id.type == 'cash':
                        if self.payment_type == 'outbound':  # Send
                            name = self.env['ir.sequence'].next_by_code('cash.payment.send.sequence') or '/'
                            # print('cash-send')
                        elif self.payment_type == 'inbound':  # Receive
                            name = self.env['ir.sequence'].next_by_code('cash.payment.receive.sequence') or '/'
                            # print('cash-receive')
                    elif self.journal_id.type == 'bank':
                        if self.payment_type == 'outbound':  # Send
                            name = self.env['ir.sequence'].next_by_code('bank.payment.send.sequence') or '/'
                            # print('bank-send')
                        elif self.payment_type == 'inbound':  # Receive
                            name = self.env['ir.sequence'].next_by_code('bank.payment.receive.sequence') or '/'
                            # print('bank-rec')

                    res.update({'custom_name': name})
        return res


class IMAccountMove(models.Model):
    _inherit = 'account.move'

    custom_name = fields.Char(
        string='Voucher No.',
        required=False,
        readonly=True,
        store=True)


class IMAccountPayment(models.Model):
    _inherit = 'account.payment'

    # new addition
    custom_name = fields.Char(
        string='Voucher No.',
        required=False,
        readonly=True,
        store=True
    )

    def action_post(self):
        res = super(IMAccountPayment, self).action_post()
        # Payment sequence for customer
        if self.env.user.company_id.id == 1:
            for rec in self:
                if rec.custom_name == False and rec.move_id.custom_name == False:
                    if rec.is_internal_transfer is False:
                        if rec.journal_id.type == 'cash':
                            if rec.payment_type == 'outbound':  # Send
                                name = self.env['ir.sequence'].next_by_code('cash.payment.send.sequence') or '/'
                                # print('cash-send')
                            elif self.payment_type == 'inbound':  # Receive
                                name = self.env['ir.sequence'].next_by_code('cash.payment.receive.sequence') or '/'
                                # print('cash-receive')

                        elif rec.journal_id.type == 'bank':
                            if rec.payment_type == 'outbound':  # Send
                                name = self.env['ir.sequence'].next_by_code('bank.payment.send.sequence') or '/'
                                # print('bank-send')

                            elif rec.payment_type == 'inbound':  # Receive
                                name = self.env['ir.sequence'].next_by_code('bank.payment.receive.sequence') or '/'
                                # print('bank-rec')
                    else:
                        name = self.env['ir.sequence'].next_by_code('internal.payment.sequence') or '/'

                    rec.move_id.custom_name = name
                    rec.custom_name = name
        return res
