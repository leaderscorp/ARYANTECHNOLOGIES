# -*- coding: utf-8 -*-
{
    'name': 'User Update On-Hand Quantity Permission',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Allow or restrict updating product on-hand quantity based on user permission checkbox',
    'description': """
User Update On-Hand Quantity Permission
=======================================
This module adds a permission checkbox on the User form (`res.users`).
If checked, the user is allowed to update product on-hand quantity.
If unchecked, the user is restricted from updating product on-hand quantity.
    """,
    'author': 'Aryan Technologies',
    'website': 'https://aryantechnologies.com',
    'depends': ['base', 'stock'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
