from odoo import fields, models, api

class CurrencyReportXlsx(models.AbstractModel):
    _name = 'report.at_prtnr_ledg_curr_rep.at_partner_ledger_currency_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):

        sheet = workbook.add_worksheet('Currency Report')
        floating_point = workbook.add_format({'num_format': '#,##0.00'})
        bold = workbook.add_format({'bold': True})

        # Define the headings
        headings = ['S#', 'Reference','Partner', 'Detail', 'Matching Currency', 'Dr', 'Cr', 'Balance', 'Rate']

        # Group data by currency
        grouped_data = {}
        for value in data['data'].values():
            currency = value['currency']
            if currency not in grouped_data:
                grouped_data[currency] = []
            grouped_data[currency].append(value)

        # Write data to sheet, separated by currency
        row = 0
        for currency, values in grouped_data.items():
            # Write currency as a section header
            row += 1
            sheet.write(row, 0, f"Currency: {currency}", bold)
            row += 1

            # Write the headings
            for col, heading in enumerate(headings):
                sheet.write(row, col, heading, bold)

            # Write the data rows and calculate totals
            total_debit = 0
            total_credit = 0
            total_balance = 0
            for sno, value in enumerate(values, start=1):
                row += 1
                sheet.write(row, 0, sno)
                sheet.write(row, 1, value['reference'])
                sheet.write(row, 2, value['partner'])
                sheet.write(row, 3, value['name'])
                sheet.write(row, 4, value['currency'])
                sheet.write(row, 5, value['debit'], floating_point)
                sheet.write(row, 6, value['credit'], floating_point)
                sheet.write(row, 7, value['balance'], floating_point)
                sheet.write(row, 8, value['currency_rate'], floating_point)

                # Update totals
                total_debit += value['debit']
                total_credit += value['credit']
                total_balance += value['balance']

            # Write the totals row
            row += 3
            sheet.write(row, 4, 'Total', bold)
            sheet.write(row, 5, total_debit, floating_point)
            sheet.write(row, 6, total_credit, floating_point)
            sheet.write(row, 7, total_balance, floating_point)

            # Add an empty row between different currency sections
            row += 5


 # print(objs.partner_id_name.name)
        # for rec in data['data']:
        #     print(rec['currency'])