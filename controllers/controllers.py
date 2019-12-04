# -*- coding: utf-8 -*-
from odoo import http

# class VitDropDana(http.Controller):
#     @http.route('/vit_drop_dana/vit_drop_dana/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_drop_dana/vit_drop_dana/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_drop_dana.listing', {
#             'root': '/vit_drop_dana/vit_drop_dana',
#             'objects': http.request.env['vit_drop_dana.vit_drop_dana'].search([]),
#         })

#     @http.route('/vit_drop_dana/vit_drop_dana/objects/<model("vit_drop_dana.vit_drop_dana"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_drop_dana.object', {
#             'object': obj
#         })