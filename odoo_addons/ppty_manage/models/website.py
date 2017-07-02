from odoo import models, fields, api
from odoo.exceptions import AccessError
from odoo.addons.ethereum_contract_odoo.models import website
import simplejson as json
import requests


class Website(website.Website):
    _inherit = 'website'

    cs_ws_url = fields.Char('Casalta WS URL')
    gmap_api_key = fields.Char('Google maps API key')

    @api.one
    def _ws(self, path, params={}, cert=False):
        resp = requests.post(url=self.cs_ws_url + '/' + path,
                             data=json.dumps(params), cert=cert,
                             headers={'Content-type': 'application/json', 'Accept': 'application/json'}, verify=False)
        resp.raise_for_status()
        return json.loads(resp.text)

    @api.one
    def cs_ws_new_account(self, eth_account, pub_key):
        return self._ws('Account/Create', {
            'account': eth_account,
            'pub_key': pub_key
        }, False)

    @api.one
    def cs_ws_list(self, point_from, point_to, user_id):
        return self._ws('Points/getPointsIn', {
            'lat1': point_from[0],
            'lon1': point_from[1],
            'lat2': point_to[0],
            'lon2': point_to[1]
        }, cert=(user_id.cs_cert, user_id.cs_priv_key))

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
            'from': contract.partner_id.eth_account,
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
            'transform': ['number', 'number', 'number', 'number', 'none', 'none']
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
    def ss_addAuth(self, instance, arg_array):
        arg_array.append({
            'from': self.eth_account,
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
    def ss_buyShare(self, instance, arg_array):
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
    def ss_sellShare(self, instance, arg_array):
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
    def ss_new(self, contract, arg_array):
        arg_array.append({
            'from': self.eth_account,
            'gas': 20000000
        })
        return self._node('executor/new', {
            'contract': json.loads(contract.value),
            'arg_array': arg_array
        })
        
