from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _name = "casalta.timeslot"

    time_from = fields.Datetime('Show up time')
    time_to = fields.Datetime('Leave time')
