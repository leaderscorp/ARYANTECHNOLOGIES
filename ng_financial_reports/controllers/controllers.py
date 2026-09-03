# -*- coding: utf-8 -*-
# from odoo import http


# class NgFinancialReports(http.Controller):
#     @http.route('/ng_financial_reports/ng_financial_reports', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ng_financial_reports/ng_financial_reports/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ng_financial_reports.listing', {
#             'root': '/ng_financial_reports/ng_financial_reports',
#             'objects': http.request.env['ng_financial_reports.ng_financial_reports'].search([]),
#         })

#     @http.route('/ng_financial_reports/ng_financial_reports/objects/<model("ng_financial_reports.ng_financial_reports"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ng_financial_reports.object', {
#             'object': obj
#         })

