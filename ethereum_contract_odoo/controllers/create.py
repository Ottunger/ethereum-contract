from odoo import http
from odoo.http import request


class ExkiDeliveryAccount(http.Controller):
    @http.route('/will/new', type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def creator(self, **post):
        will = request.env['ethereum.will'].browse(post.get('id', 0))
        will.write({
            'addr': will.addr + ',' + post.get('address', '0x0'),
        })

