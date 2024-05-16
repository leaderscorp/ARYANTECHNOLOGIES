from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Requisition(models.Model):
    _name = 'request.model'
    _description = 'Requisition Module'

    name = fields.Char(string="Requisition Number", default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('approved', 'Approved'),

    ], string="Status", default='draft')

    date_field = fields.Date(string='Date', default=lambda self: fields.Date.context_today(self))
    description = fields.Char(string="Description")

    req_from = fields.Many2one('res.users', string="Request From", default=lambda  self:self.env.user)
    req_to = fields.Many2one('res.users', string="Request To")
    req_picking_type = fields.Many2one(
        'stock.picking.type',
        string="Warehouse",
        domain=[('id', 'in', [52])],
    )
    # req_picking_type = fields.Many2one(
    #     'stock.picking.type',
    #     string="Operation Type",
    #     domain=[('id', 'in', [52])],
    # )
    req_line_ids = fields.One2many('requisition.line', 'req_id')
    location_dest_id = fields.Many2one('stock.location',
                                       domain=[('id', 'in', [28])],
                                       string='Destination Location')

    transfer_created = fields.Boolean(default=False)
    # Computed field to display the name of the requestor
    requestor_name = fields.Char(string="Requestor", related='req_from.name', readonly=True)
   
    @api.onchange('req_to')
    def prrr(self):
        print("Request To",self.req_to)



    # Computed field to display the name of the recipient
    recipient_name = fields.Char(string="Recipient", related='req_to.name', readonly=True)
    received = fields.Boolean(default=False)
    sent = fields.Boolean(default=False)

    req_transfer_id = fields.Many2one(
        'stock.picking',
        'Transfer No'
    )
    req_transfer_id_state = fields.Char(string="Transfer Order State",
                                             compute='_req_transfer_state',
                                             readonly=True)


    def _req_transfer_state(self):
        if self.req_transfer_id:
            t = self.req_transfer_id.state

            self.req_transfer_id_state = str(t)

            if self.req_transfer_id_state == 'done':
                self.state = 'approved'
        else:
            self.req_transfer_id_state = 'Transfer Order Not Created'


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            print(vals)
            vals['name'] = self.env['ir.sequence'].next_by_code('request.sequence') or _('New')
            user_id = self._context['uid']

            vals['state'] = 'sent'




        return super(Requisition, self).create(vals_list)

    @api.onchange('req_picking_type')
    def print_warehouse_ids(self):
        if self.req_picking_type:
            print(self.req_picking_type.name)

    # @api.onchange('req_line_ids', 'req_picking_type')
    # def fix_source_destination(self):
    #     operation_type = self.req_picking_type
    #     if operation_type:
    #         for line in self.req_line_ids:
    #             if operation_type.default_location_src_id:
    #                 line.location_id = operation_type.default_location_src_id.id
    #             if operation_type.default_location_dest_id:
    #                 line.location_dest_id = operation_type.default_location_dest_id.id

    # @api.onchange('req_line_ids', 'req_picking_type')
    # def fix_source_destination(self):
    #     operation_type = self.req_picking_type
    #     for line in self.req_line_ids:
    #         line.location_id = operation_type.default_location_src_id.id
    #         line.location_dest_id = operation_type.default_location_dest_id.id

    def action_approve(self):
        self.write({'state': 'approved'})
        # Additional logic for approval (e.g., send notification)
        return {'type': 'ir.actions.act_window_close'}

    def action_sent(self):
        self.write({'state': 'sent'})
        # Additional logic for sending (e.g., send notification)
        return {'type': 'ir.actions.act_window_close'}

    # @api.depends('req_transfer_id.state')
    # def state_change(self):
    #     print(f'{self.req_transfer_id = }')
    #     for rec in self:
    #         if rec.req_transfer_id and rec.req_transfer_id.state == 'done':
    #             rec.state = 'approved'



    def get_received_requisitions(self):
        print("Received",self.search([('req_to', '=', self.env.user.id)]))
        return self.search([('req_to', '=', self.env.user.id)])

    # Method to filter records for the current user's sent requisitions

    def get_sent_requisitions(self):
        print("Sent",self.search([('req_from', '=', self.env.user.id)]))
        return self.search([('req_from', '=', self.env.user.id)])

    def get_formview_action_sent(self):  # No decorator needed for Odoo < 10, implicitly recordset method for Odoo >= 10

        # Return the form view action for the current record
        action = self.env.ref('requesition_module.requisition_form_view_sent').id  # Replace with your form view action ID
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': self.id,
                'res_model': self._name,
                'views': [(action, 'form')],
                'context': self.env.context,
                }

    def get_formview_action_received(self):  # No decorator needed for Odoo < 10, implicitly recordset method for Odoo >= 10

        # Return the form view action for the current record
        action = self.env.ref('requesition_module.requisition_form_view_received').id  # Replace with your form view action ID
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': self.id,
                'res_model': self._name,
                'views': [(action, 'form')],
                'context': self.env.context,
                }
    def action_transfer(self):
        self.transfer_created = True

        transfer = self.env['stock.picking']
        # domain = [('id', '=', 52)]
        # operation_type = self.env['stock.picking.type'].search(domain)
        operation_type = self.req_picking_type


        for rec in self:
            line_list = []
            for line in rec.req_line_ids:
                line_list.append({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_quantity,
                    # 'location_id': operation_type.default_location_src_id.id,
                    # 'location_dest_id': operation_type.default_location_dest_id.id
                    'location_id': operation_type.default_location_src_id.id,
                    # 'location_dest_id': operation_type.default_location_dest_id.id
                    'location_dest_id': rec.location_dest_id
                })

            vals = {
                'picking_type_id': operation_type.id,
                'location_dest_id': rec.location_dest_id.id,
                'origin': rec.name,
                'move_ids_without_package': line_list,
            }
            transfer_record = transfer.create(vals)
            rec.req_transfer_id = transfer_record
            action = {
                'type': 'ir.actions.act_window',
                'res_id': transfer_record.id,
                'res_model': 'stock.picking',
                'view_mode': 'form',
                'context': {'stock_picking_id': transfer_record.id},
                'view_id': rec.env.ref('stock.view_picking_form').id,
            }

        print("Transfer")