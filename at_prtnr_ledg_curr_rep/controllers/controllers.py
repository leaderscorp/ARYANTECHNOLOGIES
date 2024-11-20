# -*- coding: utf-8 -*-
# from odoo import http


# class AtPrtnrLedgCurrRep(http.Controller):
#     @http.route('/at_prtnr_ledg_curr_rep/at_prtnr_ledg_curr_rep', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/at_prtnr_ledg_curr_rep/at_prtnr_ledg_curr_rep/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('at_prtnr_ledg_curr_rep.listing', {
#             'root': '/at_prtnr_ledg_curr_rep/at_prtnr_ledg_curr_rep',
#             'objects': http.request.env['at_prtnr_ledg_curr_rep.at_prtnr_ledg_curr_rep'].search([]),
#         })

#     @http.route('/at_prtnr_ledg_curr_rep/at_prtnr_ledg_curr_rep/objects/<model("at_prtnr_ledg_curr_rep.at_prtnr_ledg_curr_rep"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('at_prtnr_ledg_curr_rep.object', {
#             'object': obj
#         })
