from odoo import models, fields, api
from odoo.exceptions import ValidationError


class User(models.Model):
    _inherit = 'res.users'

    eth_account = fields.Char('Ether account')
    eth_balance = fields.Float('Ether balance')

    def create(self, vals):
        resp = self.env['website'].browse(1).new_account()
        if not 'address' in resp:
            raise ValidationError('Cannot create account, NodeJS down?')
        vals.update({
            'eth_account': resp['address'],
            'eth_balance': 0.0
        })
        return super(User, self).create(vals)
