# -*- coding: utf-8 -*-
# from odoo import http


# class ImWipRep(http.Controller):
#     @http.route('/im_wip_rep/im_wip_rep', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/im_wip_rep/im_wip_rep/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('im_wip_rep.listing', {
#             'root': '/im_wip_rep/im_wip_rep',
#             'objects': http.request.env['im_wip_rep.im_wip_rep'].search([]),
#         })

#     @http.route('/im_wip_rep/im_wip_rep/objects/<model("im_wip_rep.im_wip_rep"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('im_wip_rep.object', {
#             'object': obj
#         })
