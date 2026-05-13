{
    'name': 'Sale & Invoice Repair Link',
    'version': '19.0.1.0.0',
    'summary': 'Show Repair Number from Repair Order on Sales Order and Invoice',
    'description': """
        This module adds a computed field on Sales Order and Invoice
        to display related Repair Order sequence (seq_desc).
    """,
    'author': 'Saif',
    'category': 'Sales',
    'depends': [
        'base',
        'sale_management',
        'account',
        'repair'
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
         'views/repair_order_view.xml',
        'reports/report_saleorder.xml',
        'reports/invoice_report.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}