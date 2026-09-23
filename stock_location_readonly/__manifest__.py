{
    'name': 'Stock Location Readonly',
    'version': '19.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Makes the Quantity on Hand Locations view readonly - prevents users from editing stock quantities directly',
    'description': """
        This module makes the stock quant (Quantity on Hand) locations view readonly.
        When users click on "Quantity on Hand" from the product form and try to use
        the "New" button or edit existing records, all fields will be read-only and
        no changes can be saved.
    """,
    'author': 'Aryan Technologies',
    'depends': ['stock'],
    'data': [
        'views/stock_quant_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
