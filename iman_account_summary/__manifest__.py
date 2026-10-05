{
    'name': 'Iman Account Summary Report Fix',
    'version': '19.0.1.0.1',
    'summary': 'Fixes ACCOUNT RECEIVABLES formula in Account Summary to match Balance Sheet',
    'description': """
        This module updates the ACCOUNT RECEIVABLES line in the Account Summary report
        to show the same value as the Balance Sheet's Account Receivable (account 110000).

        Fix: Removes EMPLOYEE and RELATED PARTY exclusion filters so the full
        account 110000 balance is shown (matching the Balance Sheet).
    """,
    'author': 'Saif',
    'category': 'Accounting',
    'depends': [
        'account',
        'account_reports',
    ],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
