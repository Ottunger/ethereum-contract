from openerp import models, fields, api


class Will(models.Model):
    _name = "ethereum.will"

    name = fields.Char('Will name')
    value = fields.Text('JSON descriptor of contract')
