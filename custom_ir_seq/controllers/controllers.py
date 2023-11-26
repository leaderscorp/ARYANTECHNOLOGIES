# -*- coding: utf-8 -*-
# from odoo import http


# class CustomIrSeq(http.Controller):
#     @http.route('/custom_ir_seq/custom_ir_seq', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_ir_seq/custom_ir_seq/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_ir_seq.listing', {
#             'root': '/custom_ir_seq/custom_ir_seq',
#             'objects': http.request.env['custom_ir_seq.custom_ir_seq'].search([]),
#         })

#     @http.route('/custom_ir_seq/custom_ir_seq/objects/<model("custom_ir_seq.custom_ir_seq"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_ir_seq.object', {
#             'object': obj
#         })
