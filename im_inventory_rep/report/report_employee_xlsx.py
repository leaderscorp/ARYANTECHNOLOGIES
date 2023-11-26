# from odoo import fields, models, api
#
#
# class InventoryReportXlsx(models.AbstractModel):
#     _name = 'report.im_inventory_rep.report_inventory_xlsx'
#     _inherit = 'report.report_xlsx.abstract'
#
#     def generate_xlsx_report(self, workbook, data, employee):
#         sheet = workbook.add_worksheet('Summary')
#
#         bold = workbook.add_format({'bold': True})
#
#         headings = ['Category',
#                     'Sum of Value',
#                      ]
#         col = 0
#         for i in headings:
#             if col <= len(headings):
#                 row = 1
#                 col += 1
#                 sheet.write(row, col, i, bold)
#             # if col == len(headings):
#             else:
#                 break
#
#         emp = data['emp']
#         sno = 0
#         col = 1
#         for employees in emp:
#             sno += 1
#             row += 1
#
#             sheet.write(row, col, sno)
#             sheet.write(row, col + 2, emp['fg'])
#
