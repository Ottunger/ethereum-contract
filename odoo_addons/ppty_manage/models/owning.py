from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Owning(models.Model):
    _name = "casalta.owning"

    user_id = fields.Many2one('res.users', string='Impacted user')
    belonging_id = fields.Many2one('casalta.belonging', string='Belonging')
    share = fields.Float('Percentage owned')
    as_owner = fields.Boolean('As owner rather than interested person')
    visit_ids = fields.Many2many('casalta.timeslot', string='Requested visits')    

