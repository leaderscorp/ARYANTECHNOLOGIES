# -*- coding: utf-8 -*-
# from odoo import http


# class ImanRoRep(http.Controller):
#     @http.route('/iman_ro_rep/iman_ro_rep', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iman_ro_rep/iman_ro_rep/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iman_ro_rep.listing', {
#             'root': '/iman_ro_rep/iman_ro_rep',
#             'objects': http.request.env['iman_ro_rep.iman_ro_rep'].search([]),
#         })

#     @http.route('/iman_ro_rep/iman_ro_rep/objects/<model("iman_ro_rep.iman_ro_rep"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iman_ro_rep.object', {
#             'object': obj
#         })
