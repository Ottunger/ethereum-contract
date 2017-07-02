from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class Controller(http.Controller):
    @http.route('/map/get', type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def get(self, point_from, point_to, **post):
        return request.website.cs_ws_list(point_from, point_to, request.env.user)[0][0]
