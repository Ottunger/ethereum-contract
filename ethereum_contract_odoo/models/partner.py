from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    eth_account = fields.Char('Ether account', readonly=True)
    eth_balance = fields.Float('Ether balance', readonly=True)

    def create(self, vals):
        resp = self.env['website'].new_account()
        if not 'address' in resp:
            raise ValidationError('Cannot create account, NodeJS down?')
        vals.update({
            'eth_account': resp['address'],
            'eth_balance': 0.0
        })
        return super(Partner, self).create(vals)
