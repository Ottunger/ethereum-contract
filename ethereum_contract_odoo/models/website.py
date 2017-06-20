from odoo import models, fields, api
from odoo.exceptions import ValidationError
import os, json, requests


class Website(models.Model):
    _inherit = 'website'

    node_host = fields.Char('NodeJS Host')
    node_port = fields.Char('NodeJS Port')
    private_key = fields.Char('Path to private key for auth')
    certificate = fields.Char('Path to certificate for auth')

    @api.one
    def run_node(self):
        os.popen('nohup node ' + os.path.abspath(__file__) + '/../../node_wrapper/index.js &')

    @api.one
    def _node(self, path, params={}):
        resp = requests.post(url='https://' + self.node_host + ':' + str(self.node_port) + '/api/v1/' + path, json=params, cert=(self.certificate, self.private_key))
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
        
