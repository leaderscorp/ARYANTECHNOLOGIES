# -*- coding: utf-8 -*-
# from odoo import http


# class RequesitionModule(http.Controller):
#     @http.route('/requesition_module/requesition_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/requesition_module/requesition_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('requesition_module.listing', {
#             'root': '/requesition_module/requesition_module',
#             'objects': http.request.env['requesition_module.requesition_module'].search([]),
#         })

#     @http.route('/requesition_module/requesition_module/objects/<model("requesition_module.requesition_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('requesition_module.object', {
#             'object': obj
#         })
