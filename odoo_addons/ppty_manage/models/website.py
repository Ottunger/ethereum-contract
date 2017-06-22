from odoo import models, fields, api
from odoo.exceptions import AccessError
from odoo.addons.ethereum_contract_odoo.models import website


class Website(website.Website):
    _inherit = 'website'

    @api.one
    def sm_get(self, instance):
        return self._node('executor/execute', {
            'contract': json.loads(instance.contract_id.value),
            'contract_address': instance.addr,
            'method': 'getAllInfo',
            'arg_array': [],
            'transform': ['ido_date_number', 'iso_date_number', 'string', 'number', 'number', 'iso_date_number', 'iso_date_number', 'string', 'number', 'number', 'none', 'none', 'none', 'iso_date_number']
        })

    @api.one
    def sm_propose(self, instance, arg_array):
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
    def sm_sign(self, instance):
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
    def sm_new(self, contract, arg_array):
        arg_array.append({
            'from': self.env.user.eth_account,
            'gas': 20000000
        })
        return self._node('executor/new', {
            'contract': json.loads(contract.value),
            'arg_array': arg_array
        })

    @api.one
    def ss_get(self, instance):
        return self._node('executor/execute', {
            'contract': json.loads(instance.contract_id.value),
            'contract_address': instance.addr,
            'method': 'getAllInfo',
            'arg_array': [],
            'transform': ['number', 'number', 'number', 'number', 'none']
        })

    @api.one
    def ss_get_share(self, instance, at):
        return self._node('executor/execute', {
            'contract': json.loads(instance.contract_id.value),
            'contract_address': instance.addr,
            'method': 'share',
            'arg_array': [at],
            'transform': ['number', 'none', 'string', 'string']
        })

    @api.one
    def ss_get_authed(self, instance, at):
        return self._node('executor/execute', {
            'contract': json.loads(instance.contract_id.value),
            'contract_address': instance.addr,
            'method': 'authed',
            'arg_array': [at],
            'transform': ['number', 'none']
        })

    @api.one
    def sm_addAuth(self, instance, arg_array):
        arg_array.append({
            'from': self.env.user.eth_account,
            'gas': 500000
        })
        return self._node('executor/execute', {
            'contract': json.loads(instance.contract_id.value),
            'contract_address': instance.addr,
            'method': 'addAuth',
            'arg_array': arg_array,
            'transform': []
        })

    @api.one
    def sm_setSupervisor(self, instance, arg_array):
        arg_array.append({
            'from': self.env.user.eth_account,
            'gas': 500000
        })
        return self._node('executor/execute', {
            'contract': json.loads(instance.contract_id.value),
            'contract_address': instance.addr,
            'method': 'setSupervisor',
            'arg_array': arg_array,
            'transform': []
        })

    @api.one
    def sm_buyShare(self, instance, arg_array):
        arg_array.append({
            'from': self.env.user.eth_account,
            'gas': 500000
        })
        return self._node('executor/execute', {
            'contract': json.loads(instance.contract_id.value),
            'contract_address': instance.addr,
            'method': 'buyShare',
            'arg_array': arg_array,
            'transform': []
        })

    @api.one
    def sm_sellShare(self, instance, arg_array):
        arg_array.append({
            'from': self.env.user.eth_account,
            'gas': 500000
        })
        return self._node('executor/execute', {
            'contract': json.loads(instance.contract_id.value),
            'contract_address': instance.addr,
            'method': 'sellShare',
            'arg_array': arg_array,
            'transform': []
        })

    @api.one
    def sm_new(self, contract, arg_array):
        arg_array.append({
            'from': self.env.user.eth_account,
            'gas': 20000000
        })
        return self._node('executor/new', {
            'contract': json.loads(contract.value),
            'arg_array': arg_array
        })
        
