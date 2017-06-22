from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Product(models.Model):
    _inherit = "product.template"

    worth_ether = fields.Float('Ether worth for buying it', default=0.0)

