from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Will(models.Model):
    _name = "ethereum.will"

    name = fields.Char('Contract name')
    addr = fields.Char('Contract addresses, comma separated')
    type = fields.Selection([('will', 'Will')], 'Contract type', required=True)
    value = fields.Text('JSON descriptor of contract')

