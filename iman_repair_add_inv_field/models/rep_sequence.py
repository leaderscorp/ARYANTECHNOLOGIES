from odoo import models, fields, api



class AddSequenceInRepairOrder(models.Model):
    _inherit='repair.order'

    seq_des = fields.Char(
        string='Repairs Reference' , compute='createseqdes')


    @api.depends('seq_des')
    def createseqdes(self):
        for rec in self:
            if isinstance(rec.description, bool) and rec.description:
                rec.seq_des = rec.name
            else:
                rec.seq_des = rec.name + ' ' + (rec.description or '')

        # y = 'asf'
        #
        #
        # self.env['ir.sequence'].sudo().search([('code', '=', 'repair.order')]).write({'name': new_seq})

        # return super(AddSequenceInRepairOrder, self).create(vals)

        # record = super(AddSequenceInRepairOrder, self).create(vals)
        # for x in vals:
        #     print(x['description'])
        #
        # sequence = self.env['ir.sequence'].next_by_code('repair.order')
        #
        # sequence_name = sequence + vals['description']
        #
        # self.env['ir.sequence'].sudo().search([('code', '=', 'repair.order')]).write({'name': sequence_name})
        #
        # return record
        #
        # sequence = self.env['ir.sequence'].next_by_code('repair.order')
        # sequence_name = sequence + vals['description']
        # self.env['ir.sequence'].sudo().search([('code', '=', 'your_sequence')]).write({'name': sequence_name})
        # return super(AddSequenceInRepairOrder, self).create(vals)
# -d Emaan-Group-Test -u iman_repair_add_inv_field