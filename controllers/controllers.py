# -*- coding: utf-8 -*-
# from odoo import http


# class ManageDiego(http.Controller):
#     @http.route('/manage_diego/manage_diego', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manage_diego/manage_diego/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('manage_diego.listing', {
#             'root': '/manage_diego/manage_diego',
#             'objects': http.request.env['manage_diego.manage_diego'].search([]),
#         })

#     @http.route('/manage_diego/manage_diego/objects/<model("manage_diego.manage_diego"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manage_diego.object', {
#             'object': obj
#         })
