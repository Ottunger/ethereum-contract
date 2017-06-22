from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Photo(models.Model):
    _name = "casalta.photo"

    belonging_id = fields.Many2one('casalta.belonging', string='Belonging')
    offer_id = fields.Many2one('casalta.offer', string='Offer')
    contained = fields.Binary('File', attachment=True)

    @api.one
    @api.constrains('belonging_id', 'offer_id')
    def _single(self):
        if self.belonging_id and self.offer_id:
            raise ValidationError('Cannot be attached twice.')

    @api.multi
    def write(self, vals):
        if self.offer_id:
            if vals.get('contained', False):
                raise ValidationError('Cannot modify signed values after agreement')
        return super(Photo, self).write(vals)

