from odoo import models, fields, api
from odoo.exceptions import ValidationError


class User(models.Model):
    _inherit = 'res.users'

    eth_account = fields.Char('Ether account')
    eth_password = fields.Char('Ether password', required=True)
    eth_balance = fields.Float('Ether balance')

    @api.model
    def create(self, vals):
        resp = self.env['website'].browse(1).new_account(vals.get('eth_password', False))[0][0]
        if not 'address' in resp:
            raise ValidationError('Cannot create account, NodeJS down?')
        vals.update({
            'eth_account': resp['address'],
            'eth_balance': 0.0
        })
        return super(User, self).create(vals)

    @api.multi
    def write(self, vals):
        del vals['eth_password']
        return super(User, self).write(vals)

    @api.one
    def mine_for_ether(self, context={}):
        self.ensure_one()
        if self.env.user.id != 1:
            raise ValidationError('Only superadmin can issue those calls')
        value = context.get('value', 1)
        self.env['website'].browse(1).mine_for_ether(self.eth_account, self.eth_password, value)
        return False

    @api.one
    def update_ether(self):
        self.ensure_one()
        resp = self.env['website'].browse(1).update_ether(self.eth_account, self.eth_password)[0][0]
        if not 'balance' in resp:
            raise ValidationError('Cannot update, NodeJS down?')
        self.eth_balance = float(resp['balance'])
        return False

