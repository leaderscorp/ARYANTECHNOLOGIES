# -*- coding: utf-8 -*-
{
    'name': 'Repair Order Invoice Button',
    'version': '19.0.1.0.0',
    'summary': 'Create Invoice from Repair Order with Smart Button',
    'description': """
        Adds a "Create Invoice" button on Repair Orders.
        - Creates an invoice directly from repair.order form
        - Displays a smart button showing linked invoices count
        - Links the invoice back to the repair order
    """,
    'category': 'Repair',
    'author': 'Custom',
    'depends': ['repair', 'account'],
    'data': [
        'views/repair_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
