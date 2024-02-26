# -*- coding: utf-8 -*-
# from odoo import http


# class MkTransHideLoc(http.Controller):
#     @http.route('/mk_trans_hide_loc/mk_trans_hide_loc', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mk_trans_hide_loc/mk_trans_hide_loc/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mk_trans_hide_loc.listing', {
#             'root': '/mk_trans_hide_loc/mk_trans_hide_loc',
#             'objects': http.request.env['mk_trans_hide_loc.mk_trans_hide_loc'].search([]),
#         })

#     @http.route('/mk_trans_hide_loc/mk_trans_hide_loc/objects/<model("mk_trans_hide_loc.mk_trans_hide_loc"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mk_trans_hide_loc.object', {
#             'object': obj
#         })
