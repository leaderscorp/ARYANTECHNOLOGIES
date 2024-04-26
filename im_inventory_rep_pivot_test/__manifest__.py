# -*- coding: utf-8 -*-
{
    'name': "im_inventory_rep_pivot_test",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/action.xml',
        'views/pivot.xml',
        'views/menu_item.xml',
        'views/stock_move.xml',
        'views/stock_quant.xml',
        'views/hide_mark_as_done_from_user.xml',
        'views/hide_mo_btn.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
