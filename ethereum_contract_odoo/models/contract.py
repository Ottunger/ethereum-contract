from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _name = "ethereum.contract"

    name = fields.Char('Contract name')
    addr_ids = fields.One2many('ethereum.contract.instance', 'contract_id', string='Contract addresses', readonly=True)
    type = fields.Selection([('will', 'Will')], 'Contract type', required=True)
    value = fields.Text('JSON descriptor of contract')

class Instance(models.Model):
    _name = "ethereum.contract.instance"

    contract_id = fields.Many2one('ethereum.contract', string='Contract')
    addr = fields.Char('Address in blockchain')

