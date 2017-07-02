from odoo import models, fields, api
from odoo.exceptions import ValidationError
from .belonging import CATEGORIES
from Crypto.PublicKey import RSA


class User(models.Model):
    _inherit = "res.users"

    rrn = fields.Char('RRN Code')
    req_categ = fields.Selection(CATEGORIES, 'Desired category')
    req_price = fields.Float('Desired maximum price')
    req_sup = fields.Float('Desired minimum superficy')
    req_buy = fields.Boolean('Requesting to buy?')
    req_fur = fields.Boolean('Requesting furnished places?')

    cs_priv_key = fields.Char('Casalta WS private key')
    cs_pub_key = fields.Char('Casalta WS public key')
    cs_cert = fields.Char('Casalta WS certificate')

    @api.model
    def create(self, vals):
        key = RSA.generate(2048)
        vals.update({
            'cs_priv_key': key.exportKey('PEM'),
            'cs_pub_key': key.publickey().exportKey('OpenSSH')
        })

        resp = self.env['website'].browse(1).cs_ws_new_account(vals.get('eth_account', False), vals['cs_pub_key'])[0][0]
        if not 'certificate' in resp:
            raise ValidationError('Cannot create account, CS WS down?')
        vals.update({
            'cs_cert': resp['certificate']
        })
        return super(User, self).create(vals)

