from odoo import models, fields, api
from odoo.exceptions import AccessError
from odoo.addons.ethereum_contract_odoo.models import website


class Website(website.Website):
    _inherit = 'website'

    @api.one
    def will_get(self, instance):
        return self._node('executor/execute', {
            'contract': json.loads(instance.contract_id.value),
            'contract_address': instance.addr,
            'method': 'getAllInfo',
            'arg_array': [],
            'transform': ['date_number', 'date_number', 'number', 'number', 'iso_date_number', 'iso_date_number', 'number', 'number', 'none', 'none', 'none', 'date_number']
        })

    @api.one
    def will_propose(self, instance, arg_array):
        arg_array.append({
            'from': self.env.user.eth_account,
            'gas': 500000
        })
        return self._node('executor/execute', {
            'contract': json.loads(instance.contract_id.value),
            'contract_address': instance.addr,
            'method': 'propose',
            'arg_array': arg_array,
            'transform': []
        })

    @api.one
    def will_sign(self, instance):
        return self._node('executor/execute', {
            'contract': json.loads(instance.contract_id.value),
            'contract_address': instance.addr,
            'method': 'sign',
            'arg_array': [{
                'from': self.env.user.eth_account,
                'gas': 500000
            }],
            'transform': []
        })

    @api.one
    def will_new(self, contract, arg_array, arg_array_2):
        arg_array.append({
            'from': self.env.user.eth_account,
            'gas': 20000000
        })
        arg_array_2.append({
            'from': self.env.user.eth_account,
            'gas': 500000
        })
        return self._node('executor/new', {
            'contract': json.loads(contract.value),
            'method': 'propose',
            'arg_array': arg_array,
            'arg_array_2': arg_array_2
        })
        
