# -*- coding: utf-8 -*-
{
    'name': 'Custom Vision Tax Invoice Report',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Action function and exact Vision Industries Tax Invoice PDF layout',
    'author': 'Custom Development',
    'depends': ['account'],
    'data': [
        'report/tax_invoice_report_action.xml',
        'report/tax_invoice_report_template.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}