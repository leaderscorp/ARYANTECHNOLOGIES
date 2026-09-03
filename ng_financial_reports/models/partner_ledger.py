# -*- coding: utf-8 -*-

import json

from odoo import api, models, _, fields
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.misc import format_date, get_lang

from datetime import timedelta
from collections import defaultdict
from itertools import groupby
import markupsafe


class PartnerLedgerCustomHandler(models.AbstractModel):
    _inherit = 'account.partner.ledger.report.handler'

    def _get_custom_display_config(self):
        return {
            'templates': {
                'AccountReportLineName': 'ng_financial_reports.PartnerLedgerLineNameT',
            },
        }

    def _custom_options_initializer(self, report, options, previous_options=None):
        super()._custom_options_initializer(report, options, previous_options=previous_options)
        options['buttons'].append(
            {'name': _('PDF + PDC'), 'action': 'action_test', 'sequence': 110, 'always_show': True})

    def action_test(self, options):
        partner, col = zip(*self._query_partners(options))
        partner_ids = [p.id for p in partner if p is not None]
        date_opt = options.get('date')

        dta = []

        for p in partner_ids:
            aml = self._get_aml_values(options, [p], 0, None).get(p)
            pdc = self._get_pdc_values(options, [p]).get(p)
            aml_init_bal = list(self._get_initial_balance_values([p], options).get(p).values())[0]
            pdc_init_bal = self._get_initial_balance_pdc_values([p], options).get(p, dict())
            dta.append((aml, pdc, aml_init_bal,  pdc_init_bal))

        report_ref = self.env.ref('ng_financial_reports.action_report_pdc_full_pdf')
        data = {
            'dta': dta,
            'date_opt': date_opt,
        }
        return report_ref.report_action(self, data=data)

    def print_testt(self, options, params=None):
        dummy, partner_id = self.env['account.report']._get_model_info_from_id(params['line_id'])
        view = 'postdate_cheque.pdc_act_window'
        action = self.env['ir.actions.act_window']._for_xml_id(view)
        action['view_mode'] = 'tree,form'
        action['domain'] = [('state', '=', 'confirm')]
        action['context'] = {'create': False, 'search_default_customer_id': [partner_id]}
        return action


    def _get_initial_balance_pdc_values(self, partner_ids, options):
        # Get sums for the initial balance.
        # period: [('date' <= options['date_from'] - 1)]
        new_options = self._get_options_initial_balance(options)
        params = [
            tuple(partner_ids),
            new_options['date']['date_to'],
        ]
        query = (f"""
            SELECT
                pdcl.customer_id                    AS partner_id,
                SUM(CASE 
                    WHEN pdcl.amount > 0 THEN pdcl.amount 
                    ELSE 0 
                END)                                AS debit,
                SUM(CASE 
                    WHEN pdcl.amount < 0 THEN -pdcl.amount 
                    ELSE 0 
                END)                                AS credit,
                SUM(pdcl.amount)                    AS balance
            FROM
                postdate_cheque_line pdcl
                JOIN postdate_cheque pdc ON pdc.id = pdcl.pdc_id 
            WHERE
                pdcl.customer_id in %s
                AND pdcl.state = 'confirm'
                AND pdc.pdc_date <= %s
            GROUP BY
                pdcl.customer_id
            """)

        self._cr.execute(query, params)
        pdc_dict = { p: {} for p in partner_ids}

        for result in self._cr.dictfetchall():
            pdc_dict[result['partner_id']] = result
        return pdc_dict

    def _get_pdc_values(self, options, partners):
        pdc_dict = {p: [] for p in partners}
        params = [
            tuple(partners),
            options['date']['date_from'],
            options['date']['date_to'],
        ]
        query = f'''
            SELECT
                pdcl.id                         AS id,
                pdcl.customer_id                AS partner_id,
                pdc.name                        AS move_name,
                pdc.reference                   AS ref,
                pdc.remarks                     AS name,
                pdcl.bank_no                    AS journal_name,
                pdcl.cheque_no                  AS cheque_no,
                pdcl.cheque_date                AS cheque_date,
                pdc.pdc_date                    AS invoice_date,
                pdc.pdc_date                    AS date_maturity,
                CASE 
                    WHEN pdcl.amount > 0 THEN pdcl.amount 
                    ELSE 0 
                END                             AS debit,
                CASE 
                    WHEN pdcl.amount < 0 THEN -pdcl.amount 
                    ELSE 0 
                END                             AS credit,
                pdcl.amount                     AS balance,
                pdcl.currency_id                AS currency_id,
                pdcl.amount                     AS amount_currency
            FROM
                postdate_cheque_line pdcl
                JOIN postdate_cheque pdc ON pdc.id = pdcl.pdc_id 
            WHERE
                pdcl.customer_id in %s
                AND pdcl.state = 'confirm'
                AND pdc.pdc_date BETWEEN %s AND %s
            ORDER BY
                pdcl.id
        '''

        self._cr.execute(query, params)
        for aml_res in self._cr.dictfetchall():
            pdc_dict[aml_res['partner_id']].append(aml_res)
        return pdc_dict

    def print_repp(self, options, params=None):
        dummy, partner_id = self.env['account.report']._get_model_info_from_id(params['line_id'])
        partner = self.env['res.partner'].browse(partner_id)
        aml_init_bal = list(self._get_initial_balance_values([partner_id], options).get(partner_id).values())[0]
        aml = self._get_aml_values(options, [partner_id], 0, None).get(partner_id)
        pdc_init_bal = self._get_initial_balance_pdc_values([partner_id], options).get(partner_id)
        pdc_list = self._get_pdc_values(options, [partner_id]).get(partner_id)
        
        # Currency Name
        currency = self.env.company.currency_id
        currency_name = "PAKISTANI RUPEES" if currency.name == 'PKR' else (currency.currency_unit_label or currency.name or "").upper()
        
        # Account Code & Account Name
        account_code = partner.property_account_receivable_id.code or ""
        account_name = partner.property_account_receivable_id.name or ""
        if aml:
            for line in aml:
                if line.get('account_code'):
                    account_code = line.get('account_code')
                    account_name = line.get('account_name')
                    break
                    
        # Report Title
        report_title = "Accounts Receivable"
        if account_code:
            account_obj = self.env['account.account'].search([('code', '=', account_code)], limit=1)
            if account_obj and account_obj.account_type == 'liability_payable':
                report_title = "Accounts Payable"
                
        # Post Status
        post_status = "UNPOSTED VOUCHERS" if options.get('all_entries') else "POSTED VOUCHERS"
        
        # Format Dates
        date_opt = options.get('date') or {}
        date_from = date_opt.get('date_from')
        date_to = date_opt.get('date_to')
        from datetime import datetime
        formatted_date_from = ""
        formatted_date_to = ""
        if date_from:
            try:
                formatted_date_from = datetime.strptime(date_from, '%Y-%m-%d').strftime('%d/%m/%Y')
            except Exception:
                formatted_date_from = date_from
        if date_to:
            try:
                formatted_date_to = datetime.strptime(date_to, '%Y-%m-%d').strftime('%d/%m/%Y')
            except Exception:
                formatted_date_to = date_to
                
        # Initial balances formatting
        init_debit = aml_init_bal.get('debit', 0.0) if aml_init_bal else 0.0
        init_credit = aml_init_bal.get('credit', 0.0) if aml_init_bal else 0.0
        init_balance = aml_init_bal.get('balance', 0.0) if aml_init_bal else 0.0
        
        def format_amount(amount):
            if amount is None:
                return "0.00"
            return f"{amount:,.2f}"

        def format_bal_label(amount):
            if amount > 0:
                return f"{amount:,.2f} DR"
            elif amount < 0:
                return f"{abs(amount):,.2f} CR"
            else:
                return "0.00 DR"
                
        formatted_init_debit = format_amount(init_debit)
        formatted_init_credit = format_amount(init_credit)
        
        # AML processing
        aml_rows = []
        running_bal = init_balance
        sub_total_debit = 0.0
        sub_total_credit = 0.0
        
        if aml:
            for idx, line in enumerate(aml):
                debit = line.get('debit', 0.0) or 0.0
                credit = line.get('credit', 0.0) or 0.0
                running_bal += (debit - credit)
                sub_total_debit += debit
                sub_total_credit += credit
                
                journal_code = line.get('journal_code', '')
                payment_val = ''
                if journal_code in ['CSH', 'CASH']:
                    payment_val = 'CASH'
                elif journal_code in ['BNK', 'BANK']:
                    payment_val = 'BANK'
                    
                line_date_raw = line.get('invoice_date')
                line_date_str = ""
                if line_date_raw:
                    if isinstance(line_date_raw, str):
                        try:
                            line_date_str = datetime.strptime(line_date_raw, '%Y-%m-%d').strftime('%d/%m/%Y')
                        except Exception:
                            line_date_str = line_date_raw
                    else:
                        line_date_str = line_date_raw.strftime('%d/%m/%Y')
                        
                aml_rows.append({
                    'sno': idx + 1,
                    'date': line_date_str,
                    'voucher_no': line.get('move_name', ''),
                    'payment': payment_val,
                    'document_no': line.get('ref', '') or '',
                    'description': line.get('name', '') or '',
                    'debit': format_amount(debit),
                    'credit': format_amount(credit),
                    'balance': format_bal_label(running_bal)
                })
                
        sub_total_bal = init_balance + sub_total_debit - sub_total_credit
        formatted_sub_total_debit = format_amount(sub_total_debit)
        formatted_sub_total_credit = format_amount(sub_total_credit)
        formatted_sub_total_balance = format_bal_label(sub_total_bal)
        
        account_wise_bal = sub_total_debit - sub_total_credit
        formatted_account_wise_debit = format_amount(sub_total_debit)
        formatted_account_wise_credit = format_amount(sub_total_credit)
        formatted_account_wise_balance = f"{account_wise_bal:,.2f}"
        
        formatted_grand_total_debit = format_amount(sub_total_debit)
        formatted_grand_total_credit = format_amount(sub_total_credit)
        formatted_grand_total_balance = format_bal_label(sub_total_bal)
        
        # PDC / Un-cleared Cheque Table
        pdc_rows = []
        pdc_sub_total_debit = 0.0
        pdc_sub_total_credit = 0.0
        
        if pdc_list:
            for idx, line in enumerate(pdc_list):
                raw_debit = line.get('debit', 0.0) or 0.0
                raw_credit = line.get('credit', 0.0) or 0.0
                
                # If report_title is Accounts Receivable, customer cheque reduces receivable balance (Credits).
                # If report_title is Accounts Payable, vendor cheque reduces payable balance (Debits).
                if report_title == "Accounts Receivable":
                    debit = raw_credit
                    credit = raw_debit or raw_credit
                else:
                    debit = raw_debit or raw_credit
                    credit = raw_credit
                    
                pdc_sub_total_debit += debit
                pdc_sub_total_credit += credit
                
                cheque_date_raw = line.get('cheque_date') or line.get('invoice_date')
                cheque_date_str = ""
                if cheque_date_raw:
                    if isinstance(cheque_date_raw, str):
                        try:
                            if ' ' in cheque_date_raw:
                                cheque_date_raw = cheque_date_raw.split(' ')[0]
                            cheque_date_str = datetime.strptime(cheque_date_raw, '%Y-%m-%d').strftime('%d/%m/%Y')
                        except Exception:
                            cheque_date_str = cheque_date_raw
                    else:
                        cheque_date_str = cheque_date_raw.strftime('%d/%m/%Y')
                        
                pdc_rows.append({
                    'sno': idx + 1,
                    'date': cheque_date_str,
                    'voucher_no': line.get('move_name', ''),
                    'payment': '',
                    'document_no': line.get('cheque_no', '') or '',
                    'description': line.get('name', '') or '',
                    'debit': format_amount(debit),
                    'credit': format_amount(credit),
                    'balance': ''
                })
                
        formatted_pdc_sub_total_debit = format_amount(pdc_sub_total_debit)
        formatted_pdc_sub_total_credit = format_amount(pdc_sub_total_credit)
        
        net_after_pdc_val = sub_total_bal + (pdc_sub_total_debit - pdc_sub_total_credit)
        formatted_net_after_pdc_balance = format_bal_label(net_after_pdc_val)
        
        printed_on = fields.Datetime.context_timestamp(self, datetime.now()).strftime('%d-%m-%Y %H:%M')
        
        report_ref = self.env.ref('ng_financial_reports.action_report_pdc_pdf')
        data = {
            'report_title': report_title,
            'date_from': formatted_date_from,
            'date_to': formatted_date_to,
            'currency_name': currency_name,
            'partner_name': partner.name,
            'account_code': account_code,
            'post_status': post_status,
            'init_debit': formatted_init_debit,
            'init_credit': formatted_init_credit,
            'aml_rows': aml_rows,
            'sub_total_debit': formatted_sub_total_debit,
            'sub_total_credit': formatted_sub_total_credit,
            'sub_total_balance': formatted_sub_total_balance,
            'account_wise_debit': formatted_account_wise_debit,
            'account_wise_credit': formatted_account_wise_credit,
            'account_wise_balance': formatted_account_wise_balance,
            'grand_total_debit': formatted_grand_total_debit,
            'grand_total_credit': formatted_grand_total_credit,
            'grand_total_balance': formatted_grand_total_balance,
            
            'pdc_rows': pdc_rows,
            'pdc_sub_total_debit': formatted_pdc_sub_total_debit,
            'pdc_sub_total_credit': formatted_pdc_sub_total_credit,
            'net_after_pdc_balance': formatted_net_after_pdc_balance,
            'printed_on': printed_on,
        }
        return report_ref.report_action(self, data=data)

    def _get_aml_values(self, options, partner_ids, offset=0, limit=None):
        rslt = {partner_id: [] for partner_id in partner_ids}

        partner_ids_wo_none = [x for x in partner_ids if x]
        directly_linked_aml_partner_clauses = []
        directly_linked_aml_partner_params = []
        indirectly_linked_aml_partner_params = []
        indirectly_linked_aml_partner_clause = 'aml_with_partner.partner_id IS NOT NULL'
        if None in partner_ids:
            directly_linked_aml_partner_clauses.append('account_move_line.partner_id IS NULL')
        if partner_ids_wo_none:
            directly_linked_aml_partner_clauses.append('account_move_line.partner_id IN %s')
            directly_linked_aml_partner_params.append(tuple(partner_ids_wo_none))
            indirectly_linked_aml_partner_clause = 'aml_with_partner.partner_id IN %s'
            indirectly_linked_aml_partner_params.append(tuple(partner_ids_wo_none))
        directly_linked_aml_partner_clause = '(' + ' OR '.join(directly_linked_aml_partner_clauses) + ')'

        ct_query = self.env['account.report']._get_query_currency_table(options)
        queries = []
        all_params = []
        lang = self.env.lang or get_lang(self.env).code
        journal_name = f"COALESCE(journal.name->>'{lang}', journal.name->>'en_US')" if \
            self.pool['account.journal'].name.translate else 'journal.name'
        account_name = f"COALESCE(account.name->>'{lang}', account.name->>'en_US')" if \
            self.pool['account.account'].name.translate else 'account.name'
        report = self.env.ref('account_reports.partner_ledger_report')
        additional_columns = self._get_additional_column_aml_values()
        for column_group_key, group_options in report._split_options_per_column_group(options).items():
            tables, where_clause, where_params = report._query_get(group_options, 'strict_range')

            all_params += [
                column_group_key,
                *where_params,
                *directly_linked_aml_partner_params,
                column_group_key,
                *indirectly_linked_aml_partner_params,
                *where_params,
                group_options['date']['date_from'],
                group_options['date']['date_to'],
            ]

            # For the move lines directly linked to this partner
            queries.append(f'''
                SELECT
                    account_move_line.id,
                    account_move_line.date_maturity,
                    account_move_line.name,
                    COALESCE(NULLIF(account_move.reference_no, ''), NULLIF((SELECT so.reference_no FROM sale_order so WHERE so.name = account_move.invoice_origin LIMIT 1), ''), NULLIF(account_move_line.ref, ''), NULLIF(account_move.ref, ''), NULLIF(account_move.payment_reference, ''), account_move.invoice_origin) AS ref,
                    COALESCE(NULLIF(account_move.reference_no, ''), NULLIF((SELECT so.reference_no FROM sale_order so WHERE so.name = account_move.invoice_origin LIMIT 1), ''), NULLIF(account_move_line.ref, ''), NULLIF(account_move.ref, ''), NULLIF(account_move.payment_reference, ''), account_move.invoice_origin) AS reference_no,
                    account_move_line.company_id,
                    account_move_line.account_id,
                    account_move_line.payment_id,
                    account_move_line.partner_id,
                    account_move_line.currency_id,
                    account_move_line.amount_currency,
                    account_move_line.matching_number,
                    {additional_columns}
                    COALESCE(account_move_line.invoice_date, account_move_line.date)                 AS invoice_date,
                    ROUND(account_move_line.debit * currency_table.rate, currency_table.precision)   AS debit,
                    ROUND(account_move_line.credit * currency_table.rate, currency_table.precision)  AS credit,
                    ROUND(account_move_line.balance * currency_table.rate, currency_table.precision) AS balance,
                    account_move.name                                                                AS move_name,
                    account_move.move_type                                                           AS move_type,
                    account_move.invoice_origin                                                      AS invoice_origin,
                    account.code                                                                     AS account_code,
                    {account_name}                                                                   AS account_name,
                    journal.code                                                                     AS journal_code,
                    {journal_name}                                                                   AS journal_name,
                    %s                                                                               AS column_group_key,
                    'directly_linked_aml'                                                            AS key,
                    0                                                                                AS partial_id
                FROM {tables}
                JOIN account_move ON account_move.id = account_move_line.move_id
                LEFT JOIN {ct_query} ON currency_table.company_id = account_move_line.company_id
                LEFT JOIN res_company company               ON company.id = account_move_line.company_id
                LEFT JOIN res_partner partner               ON partner.id = account_move_line.partner_id
                LEFT JOIN account_account account           ON account.id = account_move_line.account_id
                LEFT JOIN account_journal journal           ON journal.id = account_move_line.journal_id
                WHERE {where_clause} AND {directly_linked_aml_partner_clause}
                ORDER BY account_move_line.date, account_move_line.id
            ''')

            # For the move lines linked to no partner, but reconciled with this partner. They will appear in grey in the report
            queries.append(f'''
                SELECT
                    account_move_line.id,
                    account_move_line.date_maturity,
                    account_move_line.name,
                    COALESCE(NULLIF(account_move.reference_no, ''), NULLIF((SELECT so.reference_no FROM sale_order so WHERE so.name = account_move.invoice_origin LIMIT 1), ''), NULLIF(account_move_line.ref, ''), NULLIF(account_move.ref, ''), NULLIF(account_move.payment_reference, ''), account_move.invoice_origin) AS ref,
                    COALESCE(NULLIF(account_move.reference_no, ''), NULLIF((SELECT so.reference_no FROM sale_order so WHERE so.name = account_move.invoice_origin LIMIT 1), ''), NULLIF(account_move_line.ref, ''), NULLIF(account_move.ref, ''), NULLIF(account_move.payment_reference, ''), account_move.invoice_origin) AS reference_no,
                    account_move_line.company_id,
                    account_move_line.account_id,
                    account_move_line.payment_id,
                    aml_with_partner.partner_id,
                    account_move_line.currency_id,
                    account_move_line.amount_currency,
                    account_move_line.matching_number,
                    {additional_columns}
                    COALESCE(account_move_line.invoice_date, account_move_line.date)                    AS invoice_date,
                    CASE WHEN aml_with_partner.balance > 0 THEN 0 ELSE ROUND(
                        partial.amount * currency_table.rate, currency_table.precision
                    ) END                                                                               AS debit,
                    CASE WHEN aml_with_partner.balance < 0 THEN 0 ELSE ROUND(
                        partial.amount * currency_table.rate, currency_table.precision
                    ) END                                                                               AS credit,
                    - sign(aml_with_partner.balance) * ROUND(
                        partial.amount * currency_table.rate, currency_table.precision
                    )                                                                                   AS balance,
                    account_move.name                                                                   AS move_name,
                    account_move.move_type                                                              AS move_type,
                    account_move.invoice_origin                                                         AS invoice_origin,
                    account.code                                                                        AS account_code,
                    {account_name}                                                                      AS account_name,
                    journal.code                                                                        AS journal_code,
                    {journal_name}                                                                      AS journal_name,
                    %s                                                                                  AS column_group_key,
                    'indirectly_linked_aml'                                                             AS key,
                    partial.id                                                                          AS partial_id
                FROM {tables}
                    LEFT JOIN {ct_query} ON currency_table.company_id = account_move_line.company_id,
                    account_partial_reconcile partial,
                    account_move,
                    account_move_line aml_with_partner,
                    account_journal journal,
                    account_account account
                WHERE
                    (account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id)
                    AND account_move_line.partner_id IS NULL
                    AND account_move.id = account_move_line.move_id
                    AND (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
                    AND {indirectly_linked_aml_partner_clause}
                    AND journal.id = account_move_line.journal_id
                    AND account.id = account_move_line.account_id
                    AND {where_clause}
                    AND partial.max_date BETWEEN %s AND %s
                ORDER BY account_move_line.date, account_move_line.id
            ''')

        query = '(' + ') UNION ALL ('.join(queries) + ')'

        if offset:
            query += ' OFFSET %s '
            all_params.append(offset)

        if limit:
            query += ' LIMIT %s '
            all_params.append(limit)

        self._cr.execute(query, all_params)
        for aml_result in self._cr.dictfetchall():
            if aml_result['key'] == 'indirectly_linked_aml':

                # Append the line to the partner found through the reconciliation.
                if aml_result['partner_id'] in rslt:
                    rslt[aml_result['partner_id']].append(aml_result)

                # Balance it with an additional line in the Unknown Partner section but having reversed amounts.
                if None in rslt:
                    rslt[None].append({
                        **aml_result,
                        'debit': aml_result['credit'],
                        'credit': aml_result['debit'],
                        'balance': -aml_result['balance'],
                    })
            else:
                rslt[aml_result['partner_id']].append(aml_result)

        return rslt
