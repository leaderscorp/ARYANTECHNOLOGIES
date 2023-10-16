# -*- coding: utf-8 -*-
# from odoo import http


# class ImanOpOiRep(http.Controller):
#     @http.route('/iman_op_oi_rep/iman_op_oi_rep', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iman_op_oi_rep/iman_op_oi_rep/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iman_op_oi_rep.listing', {
#             'root': '/iman_op_oi_rep/iman_op_oi_rep',
#             'objects': http.request.env['iman_op_oi_rep.iman_op_oi_rep'].search([]),
#         })

#     @http.route('/iman_op_oi_rep/iman_op_oi_rep/objects/<model("iman_op_oi_rep.iman_op_oi_rep"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iman_op_oi_rep.object', {
#             'object': obj
#         })
