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
        self.ensure_one()
        os.popen('nohup node ' + os.path.abspath(__file__) + '/../../node_wrapper/index.js &')

    @api.model
    def _node(self, path, params={}):
        resp = requests.post(url='https://' + node_host + ':' + str(node_port) + '/api/v1/' + path, json=params, cert=(self.certificate, self.private_key))
        return resp.json()

    @api.model
    def new_account(self):
        return _node('create_account')
        
