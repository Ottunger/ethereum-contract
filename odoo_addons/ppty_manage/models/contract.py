from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _inherit = "ethereum.contract"

    type = fields.Selection([
        ('will', 'Will'),
        ('sell_mandate', 'Sell Mandate'),
        ('split_sell', 'Split Sell')
    ], 'Contract type', required=True)
