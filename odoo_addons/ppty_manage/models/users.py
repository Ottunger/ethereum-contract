from odoo import models, fields, api
from odoo.exceptions import ValidationError
from .belonging import CATEGORIES


class User(models.Model):
    _inherit = "res.users"

    rrn = fields.Char('RRN Code')
    req_categ = fields.Selection(CATEGORIES, 'Desired category')
    req_price = fields.Float('Desired maximum price')
    req_sup = fields.Float('Desired minimum superficy')
    req_buy = fields.Boolean('Requesting to buy?')
    req_fur = fields.Boolean('Requesting furnished places?')

