# -*- coding: utf-8 -*-
{
    'name': "ng_financial_reports",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_reports', 'postdate_cheque'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/full_pl_pdc.xml',
        'views/report_header_override.xml',
    ],
    'assets': {
        'web.assets_backend': [
                'ng_financial_reports/static/src/components/**/*',
            ]
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

