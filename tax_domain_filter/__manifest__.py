{
    'name': 'Tax Domain Filter',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Filters taxes to show only sale taxes in sales and purchase taxes in purchases',
    'description': """
This module ensures that only Sales taxes can be selected in Sale Orders and Customer Invoices,
and only Purchase taxes can be selected in Purchase Orders and Vendor Bills.
    """,
    'author': 'Your Company',
    'depends': ['sale', 'purchase', 'account'],
    'data': [
        'views/tax_domain_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
