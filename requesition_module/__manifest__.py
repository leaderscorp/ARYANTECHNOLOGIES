# -*- coding: utf-8 -*-
{
    'name': "requesition_module",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        This is for creating requesitions
    """,

    'author': "Faisal Malik",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/req_rece.xml',
        'views/all_rec.xml',
        'views/req_sent.xml',
        'views/templates.xml',
        'views/sequence.xml',
        # 'views/access.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
'installable': True,
    'application': True,
}
