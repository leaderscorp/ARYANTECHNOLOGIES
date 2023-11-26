# -*- coding: utf-8 -*-
# from odoo import http


# class ImanPrRep(http.Controller):
#     @http.route('/iman_pr_rep/iman_pr_rep', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iman_pr_rep/iman_pr_rep/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iman_pr_rep.listing', {
#             'root': '/iman_pr_rep/iman_pr_rep',
#             'objects': http.request.env['iman_pr_rep.iman_pr_rep'].search([]),
#         })

#     @http.route('/iman_pr_rep/iman_pr_rep/objects/<model("iman_pr_rep.iman_pr_rep"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iman_pr_rep.object', {
#             'object': obj
#         })
