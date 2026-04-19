from odoo import api, fields, models
from datetime import datetime


class InventoryReport(models.TransientModel):
    _name = 'inventory.wizard.report'
    _description = 'inventory.wizard.report'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def get_report(self):
        
        domain = [('state', '=', 'done')]

        if self.date_from:
           
            domain.append(('date', '>=', fields.Datetime.to_datetime(self.date_from)))

        if self.date_to:
            
            dt_to = fields.Datetime.to_datetime(self.date_to)
            domain.append(('date', '<=', dt_to.replace(hour=23, minute=59, second=59, microsecond=999999)))

        inventory = self.env['stock.move'].search(domain)

        fg_val = fg_qty = 0.0
        ckd_val = ckd_qty = 0.0
        raw_val = raw_qty = 0.0

        for item in inventory:
        
            val = item.value or 0.0
            qty = item.product_uom_qty or 0.0

            if 1 in item.product_id.product_tag_ids.mapped('id'):
                fg_val += val
                fg_qty += qty
            elif 2 in item.product_id.product_tag_ids.mapped('id'):
                ckd_val += val
                ckd_qty += qty
            if 3 in item.product_id.product_tag_ids.mapped('id'):   
                raw_val += val
                raw_qty += qty

        data_dict = {
            'fg': fg_val,
            'fg_qty': fg_qty,
            'ckd': ckd_val,
            'ckd_qty': ckd_qty,
            'raw': raw_val,
            'raw_qty': raw_qty,
        }

        data = {'emp': data_dict}

        return self.env.ref('im_inventory_rep.im_inventory_report_xlsx_action').report_action(self, data=data)