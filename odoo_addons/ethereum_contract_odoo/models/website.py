from odoo import models, fields, api
from odoo.exceptions import AccessError
import os, json, requests


class Website(models.Model):
    _inherit = 'website'

    eth_account = fields.Char('Ether account')
    node_host = fields.Char('NodeJS Host')
    node_port = fields.Char('NodeJS Port')
    private_key = fields.Char('Path to private key for auth')
    certificate = fields.Char('Path to certificate for auth')

    @api.one
    def run_node(self):
        os.popen('nohup node ' + os.path.abspath(__file__) + '/../../node_wrapper/index.js &')

    @api.one
    def _node(self, path, params={}):
        resp = requests.post(url='https://' + self.node_host + ':' + str(self.node_port) + '/api/v1/' + path, data=json.dumps(params), cert=(self.certificate, self.private_key), headers = {'Content-type': 'application/json', 'Accept': 'application/json'}, verify=False)
        resp.raise_for_status()
        return json.loads(resp.text)

    @api.one
    def new_account(self, password):
        return self._node('create_account', {'password': password})

    @api.one
    def mine_for_ether(self, account, password, value):
        return self._node('mine', {'account': account, 'password': password, 'value': value})

    @api.one
    def update_ether(self, account):
        return self._node('balance', {'account': account})

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
        
