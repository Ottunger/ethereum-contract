from odoo import http
from odoo.http import request
import random


class ExkiDeliveryAccount(http.Controller):
    @http.route('/will/get', type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def will_get(self, instance_id, **post):
        instance = request.env['ethereum.contract.instance'].browse(instance_id)
        infos = request.env['website'].browse(1).will_get(instance)
        classname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        return {'html': request.env['ir.ui.view'].render_template('ethereum_contract_odoo.snippet_json_will', {'instance': instance, 'infos': infos, 'classname': classname}), 'classname': classname, 'signing': infos[10]}

