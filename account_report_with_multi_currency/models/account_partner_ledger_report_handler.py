# -*- coding: utf-8 -*-
from odoo import models


class AccountPartnerLedgerReportHandler(models.AbstractModel):
    _inherit = 'account.partner.ledger.report.handler'

    def _custom_options_initializer(self, report, options, previous_options):
        super()._custom_options_initializer(report, options, previous_options)
        
        # The parent method removes 'amount_currency' if user doesn't have the group.
        # We want to put it back or prevent removal.
        # Since super() runs first, it might have already removed it.
        
        # If the user does NOT have the group, super() removed it.
        # We need to add it back if it's missing.
        
        # Getting the default options again to find the column definition might be hard without re-reading the report.
        # However, typically 'amount_currency' is defined in the report's XML or base definitions.
        
        # Check if 'amount_currency' is in options['columns']
        has_amount_currency = any(col['expression_label'] == 'amount_currency' for col in options['columns'])
        
        if not has_amount_currency:
            # We need to find the definition from the report object or restore it.
            # OR we can just add a manual column definition if we know what it looks like.
            # But the report mechanism usually relies on column definitions matching specific keys.
            
            # Use report.get_table(options) logic? No, too heavy.
            
            # Let's try to fetch standard columns from the report object again?
            # Or just hackily force the group check to be ignored?
            # We can't change the group check in super().
            
            # Strategy:
            # 1. Store existing columns before super()? No, I can't wrap super easily without changing call order.
            # 2. Re-fetch columns from the report definition.
            
            # The safer way is:
            # If standard Odoo logic removed it, we re-inject it.
            # We can create a column dict that mimics the standard one.
            
            # This is the standard definition for amount_currency in partner ledger generally:
            # {
            #     'name': _('Currency'),
            #     'expression_label': 'amount_currency',
            #     'figure_type': 'monetary',
            #     'blank_if_zero': True,
            #     'column_group_key': ...
            # }
            
            # Constructing it for each column group:
            
            new_columns = []
            # We likely have debit/credit/balance columns.
            # We want to insert amount_currency usually before Balance or Debit?
            
            # Let's inspect options['columns'] structure in a running instance... I can't.
            # But I can infer.
            
            # To avoid complexity, if I can't easily restore the exact column config, 
            # I will assume that users installing this module WANT to see it, 
            # so I should try to mimic the "multi currency" group behavior.
            
            # Actually, if I inherit and override `_custom_options_initializer`, I can do:
            # options['multi_currency'] = True  <-- BEFORE super()?
            # But I can't run code before super() if I want to use super().
            # I CAN run code before super()...
            
            pass

    def _custom_options_initializer(self, report, options, previous_options):
        # Trick: Temporarily spoof the group check or ensure the flag is set so super doesn't remove it?
        # But super checks `self.env.user.has_group`. I can't easily mock that.
        
        # So I must let super run, then fix the damage.
        super()._custom_options_initializer(report, options, previous_options)
        
        # Re-enable multi_currency support flag
        options['multi_currency'] = True
        
        # Check if we need to restore columns
        has_amount_currency = any(col['expression_label'] == 'amount_currency' for col in options['columns'])
        
        if not has_amount_currency:
             # We need to re-add the columns.
             # Since traversing the whole report definition to find what was removed is hard,
             # we can look at the pattern of existing columns.
             
             # Partner ledger typically has columns per column_group.
             # We can iterate over existing column groups and add an amount_currency column.
             
             # Group existing columns by column_group_key
             from collections import defaultdict
             cols_by_group = defaultdict(list)
             for col in options['columns']:
                 cols_by_group[col['column_group_key']].append(col)
             
             restored_columns = []
             
             # We want to preserve order of groups, and insert amount_currency likely before 'balance' or at end?
             # Standard Partner Ledger order: Debit, Credit, Amount Currency, Balance (or similar).
             
             # Let's iterate through the columns and insert 'amount_currency' when we see 'balance' or appropriate spot.
             
             # But wait, we don't know the exact order defined in XML. 
             # Let's just append it to each group.
             
             sorted_cols = []
             processed_groups = set()
             
             for col in options['columns']:
                 group_key = col['column_group_key']
                 if group_key in processed_groups:
                     continue
                 
                 group_cols = cols_by_group[group_key]
                 processed_groups.add(group_key)
                 
                 # Add the group's columns, inserting amount_currency
                 # Let's check if we can copy a 'debit' column style
                 
                 current_group_new_cols = []
                 for g_col in group_cols:
                     current_group_new_cols.append(g_col)
                     
                     # Insert after Credit or Debit?
                     # Let's insert after 'credit' usually.
                     if g_col['expression_label'] == 'credit':
                         amount_curr_col = g_col.copy()
                         amount_curr_col.update({
                             'name': _('Amount Currency'),
                             'expression_label': 'amount_currency',
                             'figure_type': 'monetary',
                             'blank_if_zero': True,
                         })
                         current_group_new_cols.append(amount_curr_col)
                 
                 sorted_cols.extend(current_group_new_cols)
             
             options['columns'] = sorted_cols

