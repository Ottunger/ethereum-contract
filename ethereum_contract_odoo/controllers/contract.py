from odoo import http
from odoo.http import request
import random, string


class ExkiDeliveryAccount(http.Controller):
    @http.route('/will/get', type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def will_get(self, instance_id, **post):
        instance = request.env['ethereum.contract.instance'].browse(instance_id)
        infos = request.env['website'].browse(1).will_get(instance)
        classname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        return {'html': request.env['ir.ui.view'].render_template('ethereum_contract_odoo.snippet_json_will', {'instance': instance, 'infos': infos, 'classname': classname}), 'classname': classname, 'signing': infos[10]}

    @http.route('/will/propose', type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def will_propose(self, instance_id, arg_array, **post):
        instance = request.env['ethereum.contract.instance'].browse(instance_id)
        return request.env['website'].browse(1).will_propose(instance, arg_array)

    @http.route('/will/sign', type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def will_sign(self, instance_id, **post):
        instance = request.env['ethereum.contract.instance'].browse(instance_id)
        return request.env['website'].browse(1).will_sign(instance)

    @http.route('/will/new', type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def will_new(self, arg_array, **post):
        contract = request.env['ethereum.contract'].search([('type', '=', 'will')])[0]
        resp = request.env['website'].browse(1).will_new(contract, arg_array)
        if 'address' in resp:
            request.env['ethereum.contract.instance'].create({
                'contract_id': contract.id,
                'addr': resp['address']
            })
        return resp

