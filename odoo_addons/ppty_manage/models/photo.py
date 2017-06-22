from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Photo(models.Model):
    _name = "casalta.photo"

    belonging_id = fields.Many2one('casalta.belonging', string='Belonging')
    image = fields.Binary('Image', attachment=True)
