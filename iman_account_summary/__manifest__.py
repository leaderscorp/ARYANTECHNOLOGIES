{
    'name': 'Iman Account Summary Report Fix',
    'version': '19.0.1.0.2',
    'summary': 'Account Summary: Receivable (positive) & Payable (negative) from Partner Ledger',
    'description': """
        This module updates ACCOUNT RECEIVABLES and ACCOUNT PAYABLES lines
        in the Account Summary report to match Partner Ledger values:

        - ACCOUNT RECEIVABLE: asset_receivable accounts with 'sum'
          Shows POSITIVE values (same as Partner Ledger)

        - ACCOUNT PAYABLE: liability_payable accounts with '-sum'
          Shows NEGATIVE values (same as Partner Ledger)
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
