# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.tools import SQL


class AccountTrialBalanceReportHandler(models.AbstractModel):
    _inherit = 'account.trial.balance.report.handler'

    def _custom_options_initializer(self, report, options, previous_options):
        super()._custom_options_initializer(report, options, previous_options)
        
        # Add new columns for Amount Currency and Currency
        # checking if they already exist to avoid duplication if run multiple times or extended elsewhere
        
        has_amount_currency = False
        for column in options['columns']:
            if column['expression_label'] == 'amount_currency':
                has_amount_currency = True
                break
        
        if not has_amount_currency:
            # We want to insert these before the 'debit' column usually
            # But 'columns' structure depends on the report definition.
            # Typically for Trial Balance: Initial Balance, Debit, Credit, End Balance.
            # We want it per section (Initial, Period, End) or just generally? 
            # The Trial Balance structure is complex because it has dynamic columns per period/initial/end.
            # However, looking at _get_column_values in the parent, it seems to define columns dynamically.
            # Let's try to add a global availability first.
            
            # Actually, _custom_options_initializer in parent rebuilds options['columns'].
            # We should inject our extra columns into the definitions used there, 
            # OR modify the options['columns'] AFTER parent returns.
            
            # The parent _custom_options_initializer logic sets options['columns'] based on column groups.
            # We need to make sure our columns are added to the column definitions.
            
            # Let's inspect how columns are structured.
            # Typically: [{'name': 'Debit', 'expression_label': 'debit', ...}, ...]
            
            # We will add 'Amount Currency' and 'Currency' to each column group that makes sense (Initial, Period, End).
            # But wait, Trial Balance usually sums up Debits and Credits. 
            # 'Amount Currency' makes sense as a balance (Initial Amount Currency, Period Amount Currency, End Amount Currency).
            
            # For simplicity and standard Odoo report extension, we often augment the `columns` list.
            # However, since Trial Balance builds columns dynamically (initial, period, end), we might need to be careful.
            
            pass 
            # The actual injection needs to happen closer to where columns are generated if we want them in every section
            # Or we can just append them if we want them generally, but Trial Balance has specific column groups.

            # Alternative: Override `_get_column_values` or similar?
            # Creating columns here might be too late if `_get_column_values` already ran in super.
            # Super calls `_get_column_values` and sets `options['columns']`.
            # So modifying `options['columns']` here IS correct.
            
            new_columns = []
            for col in options['columns']:
                new_columns.append(col)
                # If we see a 'Balance' or 'Credit' column, maybe we add ours?
                # A safer bet is adding "Amount Currency" column for each block (Initial, Period, End)
                # But matching them to the right group is tricky without more logic.
                
                # Let's look at how Account General Ledger does it. It just has them.
                # Trial Balance is different.
                
                # Let's try a simple approach: 
                # Find the column keys and add Amount Currency to them.
                
                # If we just want a "Currency" column, often it's just one column for the line indicating the account currency.
                # "Amount Currency" however changes over periods.
                
            # LET'S RE-EVALUATE: 
            # If we want "Amount Currency" alongside Debit/Credit/Balance, we need it for Initial, Period, and End.
            
            # For now, let's implement the 'Currency_ID' retrieval in the engine first, 
            # and maybe just add one "Currency" column to identify the account's foreign currency.
            pass

    def _report_custom_engine_trial_balance(self, expressions, options, date_scope, current_groupby, next_groupby, offset=0, limit=None, warnings=None):
        res = super()._report_custom_engine_trial_balance(expressions, options, date_scope, current_groupby, next_groupby, offset, limit, warnings)
        
        # This function returns a list of results (or a single dictionary for totals).
        # We need to ensure 'amount_currency' is fetched.
        
        # The parent executes the query. We might need to inject our selection.
        # But the parent constructs the query inside the method.
        # To add 'amount_currency', we might need to fully override this method.
        
        # Looking at the original code in `account_trial_balance_report.py`:
        # It defines `select_balance`, `select_debit`, `select_credit`.
        # It DOES NOT select `amount_currency`.
        # We MUST override `_report_custom_engine_trial_balance` to include `amount_currency`.
        
        return res

    # Re-implementing _report_custom_engine_trial_balance with amount_currency support
    def _report_custom_engine_trial_balance(self, expressions, options, date_scope, current_groupby, next_groupby, offset=0, limit=None, warnings=None):
        report = self.env['account.report'].browse(options['report_id'])
        current_groupbys = [current_groupby] if current_groupby and not isinstance(current_groupby, list) else current_groupby or []
        report._check_groupby_fields(current_groupbys)

        if 'id' in current_groupbys and options['trial_balance_column_type'] == 'initial_balance':
            return []

        extra_domain = []
        if fiscalyear_start := options.get('trial_balance_block_fiscalyear_start'):
            extra_domain = [
                '|',
                ('account_id.include_initial_balance', '=', True),
                ('date', '>=', fiscalyear_start),
            ]

        if options.get('export_mode') == 'print' and options.get('filter_search_bar'):
             if options.get('hierarchy'):
                extra_domain += [
                    '|',
                    ('account_id', 'ilike', options['filter_search_bar']),
                    ('account_id', 'in', SQL(
                        """
                        (SELECT distinct account_account.id
                        FROM account_account
                        LEFT JOIN account_group ON
                            (
                                LEFT(account_account.code_store->> '%(company_id)s', LENGTH(code_prefix_start)) BETWEEN
                                    code_prefix_start
                                AND code_prefix_end
                            )
                        WHERE ( account_group.name->> %(lang)s  ILIKE %(filter_search_bar)s
                            OR  account_group.code_prefix_start ILIKE %(filter_search_bar)s)
                        )""",
                        lang=self.env.lang,
                        company_id=self.env.company.id,
                        filter_search_bar="%" + options['filter_search_bar'] + "%")),
                ]
             else:
                extra_domain.append(('account_id', 'ilike', options['filter_search_bar']))

        next_groupbys = next_groupby.split(',') if next_groupby else []
        query = report._get_report_query(options, date_scope, domain=extra_domain)

        if current_groupbys:
            select_groupby_key_components = SQL('\n').join(
                SQL("%s AS %s,", self.env['account.move.line']._field_to_sql("account_move_line", groupby_key, query), SQL.identifier(f'groupby_key_{groupby_key}'))
                for groupby_key in current_groupbys
            )
            query.groupby = SQL(',').join(SQL.identifier(f'groupby_key_{groupby_key}') for groupby_key in current_groupbys)

        # OVERRIDE: Added amount_currency and currency_id selection
        sql_query = SQL(
            """
            SELECT
                %(select_groupby_key_components)s
                COALESCE(SUM(%(select_balance)s), 0.0) AS balance,
                COALESCE(SUM(%(select_debit)s), 0.0) AS debit,
                COALESCE(SUM(%(select_credit)s), 0.0) AS credit,
                COALESCE(SUM(account_move_line.amount_currency), 0.0) AS amount_currency
            FROM %(table_references)s
            %(currency_table_join)s
            WHERE %(search_condition)s
            %(groupby_clause)s
            """,
            select_groupby_key_components=select_groupby_key_components if current_groupbys else SQL(''),
            select_balance=report._currency_table_apply_rate(SQL("account_move_line.balance")),
            select_debit=report._currency_table_apply_rate(SQL("account_move_line.debit")),
            select_credit=report._currency_table_apply_rate(SQL("account_move_line.credit")),
            table_references=query.from_clause,
            currency_table_join=report._currency_table_aml_join(options),
            search_condition=query.where_clause,
            groupby_clause=SQL("GROUP BY %s", query.groupby) if query.groupby else SQL(),
        )

        self.env.cr.execute(sql_query)
        query_results = self.env.cr.dictfetchall()

        disable_expand = bool((not next_groupby or next_groupbys[0] == 'id') and options['trial_balance_column_type'] == 'initial_balance')

        if not current_groupbys:
            if not query_results:
                return {
                    'balance': 0.0,
                    'debit': 0.0,
                    'credit': 0.0,
                    'amount_currency': 0.0, # Added default
                    'has_sublines': False,
                }

            query_result = query_results[0]
            query_result['has_sublines'] = True
            return query_result

        return [
            (
                (
                    query_result[f'groupby_key_{current_groupbys[0]}']
                    if len(current_groupbys) == 1
                    else tuple(query_result[f'groupby_key_{groupby}'] for groupby in current_groupbys)
                ),
                {**query_result, 'has_sublines': not disable_expand},
            )
            for query_result in query_results
        ]

    def _custom_options_initializer(self, report, options, previous_options):
        super()._custom_options_initializer(report, options, previous_options=previous_options)
        
        # Inject Amount Currency columns
        # We need to find where to insert them. 
        # Typically we have Debit, Credit, Balance.
        
        # Let's iterate over column groups to know where to add columns
        # options['columns'] contains the list of actual columns to render.
        
        new_columns = []
        for col in options['columns']:
            new_columns.append(col)
            # If this is the last column of a group (like 'balance' or 'credit'), add 'amount_currency'
            # Check expression_label
            if col['expression_label'] in ('balance', 'credit'): 
                # Avoid adding multiple times if both exist in same group??
                # Actually, each column belongs to a column_group_key.
                # We want one 'Amount Currency' per column group?
                pass
        
        # Better approach: 
        # 1. Allow 'amount_currency' expression in the report definition (which we can't easily change via Python only without loading XML).
        # OR
        # 2. Manually append columns to `options['columns']`.
        
        # Since we are in the handler, we can manipulate `options['columns']`.
        # We need to construct the column dictionary.
        
        # Group columns by column_group_key
        from collections import defaultdict
        cols_by_group = defaultdict(list)
        for col in options['columns']:
            cols_by_group[col['column_group_key']].append(col)
            
        final_columns = []
        # Reconstruct preserving order
        seen_groups = set()
        for col in options['columns']:
            group_key = col['column_group_key']
            if group_key in seen_groups:
                continue
            seen_groups.add(group_key)
            
            group_cols = cols_by_group[group_key]
            final_columns.extend(group_cols)
            
            # Create Amount Currency column for this group
            # We base it on the last column of the group to copy styles/classes
            base_col = group_cols[-1]
            
            amount_currency_col = base_col.copy()
            amount_currency_col.update({
                'name': _('Amount Currency'),
                'expression_label': 'amount_currency',
                'figure_type': 'monetary',
                # We need to ensure specific formatting if needed
            })
            final_columns.append(amount_currency_col)
            
        options['columns'] = final_columns

