# -*- coding: utf-8 -*-
# from odoo import http


# class ImInventoryRep(http.Controller):
#     @http.route('/im_inventory_rep_pivot_test/im_inventory_rep_pivot_test', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/im_inventory_rep_pivot_test/im_inventory_rep_pivot/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('im_inventory_rep_pivot.listing', {
#             'root': '/im_inventory_rep_pivot/im_inventory_rep_pivot',
#             'objects': http.request.env['im_inventory_rep_pivot.im_inventory_rep_pivot'].search([]),
#         })

#     @http.route('/im_inventory_rep_pivot/im_inventory_rep_pivot/objects/<model("im_inventory_rep_pivot.im_inventory_rep_pivot"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('im_inventory_rep_pivot.object', {
#             'object': obj
#         })
