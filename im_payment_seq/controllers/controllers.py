# -*- coding: utf-8 -*-
# from odoo import http


# class MkPaymentSeq(http.Controller):
#     @http.route('/im_payment_seq/im_payment_seq', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/im_payment_seq/im_payment_seq/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('im_payment_seq.listing', {
#             'root': '/im_payment_seq/im_payment_seq',
#             'objects': http.request.env['im_payment_seq.im_payment_seq'].search([]),
#         })

#     @http.route('/im_payment_seq/im_payment_seq/objects/<model("im_payment_seq.im_payment_seq"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('im_payment_seq.object', {
#             'object': obj
#         })
