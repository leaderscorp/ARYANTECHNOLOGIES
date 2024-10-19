from odoo import fields, api, models
from datetime import datetime

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

#     def action_post(self):
#         res = super(IMAccountPayment, self).action_post()
#
#         # Payment sequence for customer
#         for rec in self:
#             if rec.custom_name is False and rec.move_id.custom_name is False:
#                 if rec.is_internal_transfer is False:
#                     if rec.journal_id.type == 'cash':
#                         if rec.payment_type == 'outbound':  # Send
#                             sequence_code = 'cash.payment.send.sequence'
#                         elif rec.payment_type == 'inbound':  # Receive
#                             sequence_code = 'cash.payment.receive.sequence'
#                     elif rec.journal_id.type == 'bank':
#                         if rec.payment_type == 'outbound':  # Send
#                             sequence_code = 'bank.payment.send.sequence'
#                         elif rec.payment_type == 'inbound':  # Receive
#                             sequence_code = 'bank.payment.receive.sequence'
#                 else:
#                     sequence_code = 'internal.payment.sequence'
#
#                 # Generate sequence based on year and month from create_date
#                 name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code(sequence_code) or '/'
#
#                 if not rec.move_id.custom_name:
#                     rec.move_id.custom_name = name
#                 if not rec.custom_name:
#                     rec.custom_name = name
#
#         return res
#
#     @api.returns('self', lambda value: value.id)
#     def copy(self, default=None):
#         if default is None:
#             default = {}
#
#         if not default.get('custom_name'):
#             default['custom_name'] = None
#
#         return super(IMAccountPayment, self).copy(default=default)


    def action_post(self):
        res = super(IMAccountPayment, self).action_post()
        # Payment sequence for customer
        if self.env.user.company_id.id == 1 and self.env.company.id == 1:
            for rec in self:
                if rec.custom_name == False and rec.move_id.custom_name == False:
                    if rec.is_internal_transfer is False:
                        if rec.journal_id.type == 'cash':
                            if rec.payment_type == 'outbound':  # Send
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('cash.payment.send.sequence') or '/'
                                # print('cash-send')
                            elif self.payment_type == 'inbound':  # Receive
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('cash.payment.receive.sequence') or '/'
                                # print('cash-receive')

                        elif rec.journal_id.type == 'bank':
                            if rec.payment_type == 'outbound':  # Send
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('bank.payment.send.sequence') or '/'
                                # print('bank-send')

                            elif rec.payment_type == 'inbound':  # Receive
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('bank.payment.receive.sequence') or '/'
                                # print('bank-rec')
                    else:
                        name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('internal.payment.sequence') or '/'

                    # rec.move_id.custom_name = name
                    # rec.custom_name = name
                    if not rec.move_id.custom_name:
                        rec.move_id.custom_name = name
                    if not rec.custom_name:
                        rec.custom_name = name
        if self.env.user.company_id.id == 2 and self.env.company.id == 2:
            for rec in self:
                if rec.custom_name == False and rec.move_id.custom_name == False:
                    if rec.is_internal_transfer is False:
                        if rec.journal_id.type == 'cash':
                            if rec.payment_type == 'outbound':  # Send
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('at.cash.payment.send.sequence') or '/'
                                # print('cash-send')
                            elif self.payment_type == 'inbound':  # Receive
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('at.cash.payment.receive.sequence') or '/'
                                # print('cash-receive')

                        elif rec.journal_id.type == 'bank':
                            if rec.payment_type == 'outbound':  # Send
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('at.bank.payment.send.sequence') or '/'
                                # print('bank-send')

                            elif rec.payment_type == 'inbound':  # Receive
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('at.bank.payment.receive.sequence') or '/'
                                # print('bank-rec')
                    else:
                        name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('at.internal.payment.sequence') or '/'

                    # rec.move_id.custom_name = name
                    # rec.custom_name = name
                    if not rec.move_id.custom_name:
                        rec.move_id.custom_name = name
                    if not rec.custom_name:
                        rec.custom_name = name
        if self.env.company.id == 4:
            for rec in self:
                if rec.custom_name == False and rec.move_id.custom_name == False:
                    if rec.is_internal_transfer is False:
                        if rec.journal_id.type == 'cash':
                            if rec.payment_type == 'outbound':  # Send
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('gc.cash.payment.send.sequence') or '/'
                            elif self.payment_type == 'inbound':  # Receive
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('gc.cash.payment.receive.sequence') or '/'
                        elif rec.journal_id.type == 'bank':
                            if rec.payment_type == 'outbound':  # Send
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('gc.bank.payment.send.sequence') or '/'
                            elif rec.payment_type == 'inbound':  # Receive
                                name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('gc.bank.payment.receive.sequence') or '/'
                    else:
                        name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.date).next_by_code('gc.internal.payment.sequence') or '/'

                    # rec.move_id.custom_name = name
                    # rec.custom_name = name
                    if not rec.move_id.custom_name:
                        rec.move_id.custom_name = name
                    if not rec.custom_name:
                        rec.custom_name = name

        return res

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        if not default.get('custom_name'):
            default['custom_name'] = None

        return super(IMAccountPayment, self).copy(default=default)
