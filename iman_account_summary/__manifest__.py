{
    'name': 'Iman Account Summary Report',
    'version': '19.0.1.0.0',
    'summary': 'Account Summary Report for Iman Company',
    'description': """
        Defines the Account Summary report for Iman company.
        - BANK AND CASH BALANCE
        - ACCOUNT RECEIVABLES (same formula as Balance Sheet)
        - EARNEST MONEY
        - PERFORMANCE BOND
        - ADVANCES TO EMPLOYEES
        - PREPAYMENT
        - INVESTMENT
        - ACCOUNT PAYABLES
        - STOCK VALUATION
        - Due to related party
        - Total
    """,
    'author': 'Saif',
    'category': 'Accounting',
    'depends': [
        'account',
        'account_reports',
    ],
    'data': [
        'data/account_summary_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
