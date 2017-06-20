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
        return resp.json()

    @api.one
    def new_account(self):
        return self._node('create_account')

    @api.one
    def will_get(self, instance):
        return self._node('will/execute', {
            'contract': instance.contract_id.value,
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
        return self._node('will/execute', {
            'contract': instance.contract_id.value,
            'contract_address': instance.addr,
            'method': 'propose',
            'arg_array': arg_array,
            'transform': []
        })

    @api.one
    def will_sign(self, instance):
        return self._node('will/execute', {
            'contract': instance.contract_id.value,
            'contract_address': instance.addr,
            'method': 'sign',
            'arg_array': [{
                'from': self.env.user.eth_account,
                'gas': 500000
            }],
            'transform': []
        })

    @api.one
    def will_new(self, contract, arg_array):
        arg_array.append({
            'from': self.env.user.eth_account,
            'gas': 20000000
        })
        return self._node('will/new', {
            'contract': contract.value,
            'arg_array': arg_array
        })
        
