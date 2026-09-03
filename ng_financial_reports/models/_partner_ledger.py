# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PartnerLedgerCustomHandler(models.AbstractModel):
    _inherit = 'account.partner.ledger.report.handler'

    def _custom_line_postprocessor(self, report, options, lines, warnings=None):
        lines = super()._custom_line_postprocessor(report, options, lines, warnings=warnings)
        # print(f"\n_custom_line_postprocessor")
        # print(f"{options=}")
        # print(f"{lines=} \n")
        # print(f"{lines[0]=} \n")
        # print(f"{lines[1]=} \n")
        return lines


    # def _build_partner_lines(self, report, options, level_shift=0):
    #     res = super()._build_partner_lines(report, options, level_shift=0)
    #     print(f"\n _build_partner_lines")
    #     # print(f"{res[0]} \n")
    #     for l in res[0]:
    #         print(l)
    #         col = l.get('columns')
    #         print(col)
    #         for c in col:
    #             print(c)
    #         print('\n')
    #     # print(f"{res[1]}")
    #     return res

    def _report_expand_unfoldable_line_partner_ledger_pdc(self, line_dict_id, groupby, options, progress, offset, unfold_all_batch_data=None):
        print('wwwww')
        print(line_dict_id)
        print(groupby)
        print(options)
        print(progress)
        lines = []
        lines.append(self._add_custom_pdc_line(line_dict_id, options))

        return {
            'lines': lines,
            'offset_increment': 0,
            'has_more': False,
            'progress': False
        }

        pass

    def _report_expand_unfoldable_line_partner_ledger(self, line_dict_id, groupby, options, progress, offset, unfold_all_batch_data=None):
        res = super()._report_expand_unfoldable_line_partner_ledger(line_dict_id, groupby, options, progress, offset, unfold_all_batch_data=None)
        # print(f"{line_dict_id=}")
        print(f"{res=}")
        res['lines'].append(self._add_custom_pdc(line_dict_id, options))
        return res


    def _add_custom_pdc(self, line_dict_id, options):
        report = self.env['account.report'].browse(options['report_id'])
        col_vals = []
        for column in options['columns']:
            value = ''
            cols = report._build_column_dict(value, column, options=options)
            col_vals.append(cols)
        return {
            # 'id': report._get_generic_line_id('account.move.line', aml_query_result['id'],
            #                                   parent_line_id=line_dict_id),

            'id': '~account.report~13|~res.partner~367|~postdate.cheque~1',
            'parent_id': line_dict_id,
            'name': 'PDC',
            'columns': col_vals,
            'caret_options': 'postdate.cheque',
            'unfoldable': True,
            'level': 4 ,
            'expand_function': '_report_expand_unfoldable_line_partner_ledger_pdc',

        }
    def _add_custom_pdc_line(self, line_dict_id, options):
        report = self.env['account.report'].browse(options['report_id'])
        col_vals = []
        for column in options['columns']:
            col_expr_label = column['expression_label']
            if col_expr_label == 'balance':
                value = 100
            else:
                value = ''
            cols = report._build_column_dict(value, column, options=options)
            # print(cols)
            col_vals.append(cols)
        return {
            # 'id': report._get_generic_line_id('account.move.line', aml_query_result['id'],
            #                                   parent_line_id=line_dict_id),

            'id': '~account.report~13|~res.partner~367|~postdate.cheque.line~1',
            'parent_id': line_dict_id,
            'name': 'PDC',
            'columns': col_vals,
            'caret_options': 'postdate.cheque.line',
            'level': 5 ,

        }