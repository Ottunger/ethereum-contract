from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import random, string


class Controller(http.Controller):
    @http.route('/will/get', type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def get(self, instance_id, **post):
        instance = request.env['ethereum.contract.instance'].browse(instance_id)
        infos = request.website.will_get(instance)[0][0]
        classname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        return {'html': request.env['ir.ui.view'].render_template('ethereum_contract_odoo.snippet_json_will', {'instance': instance, 'infos': infos, 'classname': classname}), 'classname': classname, 'signing': infos[10]}

    @http.route('/will/propose', type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def propose(self, instance_id, arg_array, **post):
        instance = request.env['ethereum.contract.instance'].browse(instance_id)
        return request.website.will_propose(instance, arg_array)[0][0]

    @http.route('/will/sign', type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def sign(self, instance_id, **post):
        instance = request.env['ethereum.contract.instance'].browse(instance_id)
        return request.website.will_sign(instance)[0][0]

    @http.route('/will/new', type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def new(self, arg_array, arg_array_2, **post):
        contract = request.env['ethereum.contract'].search([('type', '=', 'will')])
        if len(contract) == 0:
            raise ValidationError('No contract matching type defined')
        resp = request.website.will_new(contract[0], arg_array, arg_array_2)[0][0]
        if resp.get('address', None) is not None:
            request.env['ethereum.contract.instance'].create({
                'contract_id': contract.id,
                'addr': resp['address']
            })
        return resp

