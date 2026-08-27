{
    'name': 'Hide Physical Inventory Menu',
    'version': '19.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Hide Physical Inventory Menu for Specific Users based on a checkbox',
    'description': """
        This module adds a checkbox to the user form to hide the Physical Inventory menu.
        When checked, the Physical Inventory menu will be hidden for that specific user.
    """,
    'depends': ['base', 'stock'],
    'data': [
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
