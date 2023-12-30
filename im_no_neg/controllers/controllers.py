# -*- coding: utf-8 -*-
# from odoo import http


# class ImNoNeg(http.Controller):
#     @http.route('/im_no_neg/im_no_neg', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/im_no_neg/im_no_neg/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('im_no_neg.listing', {
#             'root': '/im_no_neg/im_no_neg',
#             'objects': http.request.env['im_no_neg.im_no_neg'].search([]),
#         })

#     @http.route('/im_no_neg/im_no_neg/objects/<model("im_no_neg.im_no_neg"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('im_no_neg.object', {
#             'object': obj
#         })
