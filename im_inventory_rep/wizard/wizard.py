from odoo import api, fields, models


class InventoryReport(models.TransientModel):
    _name = 'inventory.wizard.report'
    _description = 'inventory.wizard.report'

    date_from = fields.Date(
        string='Date From'
    )
    date_to = fields.Date(
        string='Date To'
    )

    def get_report(self):
        inventory = self.env['stock.valuation.layer'].search([
            ('create_date', '>=', self.date_from),
            ('create_date', '<=', self.date_to)
        ])
        data_dict = {}
        fg_val =0
        fg_qty =0
        ckd_val =0
        ckd_qty =0
        raw_val =0
        raw_qty =0
        for item in inventory:
            if 1 in item.product_id.product_tag_ids.mapped('id'):
                fg_val += item.value
                fg_qty += item.quantity
            elif 2 in item.product_id.product_tag_ids.mapped('id'):
                ckd_val += item.value
                ckd_qty += item.quantity
            if 3 in item.product_id.product_tag_ids.mapped('id'):
                raw_val += item.value
                raw_qty += item.quantity
        data_dict = {
            'fg': fg_val,
            'fg_qty': fg_qty,
            'ckd': ckd_val,
            'ckd_qty': ckd_qty,
            'raw': raw_val,
            'raw_qty': raw_qty,
        }
        # print(data_dict)

        data = {
            'emp': data_dict
        }
        return self.env.ref('im_inventory_rep.im_inventory_report_xlsx_action').report_action(self, data=data)

