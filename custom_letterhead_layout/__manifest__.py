{
    'name': 'Vision Industries - Custom Letterhead',
    'version': '19.0.1.0.0',
    'category': 'Reporting',
    'summary': 'Adds fixed top/bottom letterhead bars to all PDF reports (header & footer)',
    'description': """
        This module injects the company letterhead (top navy bar with logo,
        bottom navy bar with contact info) into the standard wkhtmltopdf
        header/footer regions so it repeats correctly on every page,
        regardless of report content length.

        Unlike the "Background Image" option in Document Layout, this uses
        Odoo's native header/footer mechanism (div.header / div.footer),
        which wkhtmltopdf pins to a fixed position on every printed page.
    """,
    'author': 'System Nexgen',
    'depends': ['web'],
    'data': [
        'views/report_layout.xml',
    ],
    'assets': {},
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
