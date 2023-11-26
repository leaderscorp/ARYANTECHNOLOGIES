# -*- coding: utf-8 -*-
# from odoo import http


# class ImInventoryRep(http.Controller):
#     @http.route('/im_inventory_rep/im_inventory_rep', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/im_inventory_rep/im_inventory_rep/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('im_inventory_rep.listing', {
#             'root': '/im_inventory_rep/im_inventory_rep',
#             'objects': http.request.env['im_inventory_rep.im_inventory_rep'].search([]),
#         })

#     @http.route('/im_inventory_rep/im_inventory_rep/objects/<model("im_inventory_rep.im_inventory_rep"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('im_inventory_rep.object', {
#             'object': obj
#         })
