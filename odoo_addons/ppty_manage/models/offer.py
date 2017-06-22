from odoo import models, fields, api
from odoo.exceptions import ValidationError
import hashlib


class Offer(models.Model):
    _name = 'casalta.offer'

    sha256 = fields.Char('Validation tag', compute='_compute_hash', store=True)
    belonging_ids = fields.One2many('casalta.belonging', 'offer_id', string='Offers')
    user_id = fields.Many2one('res.users', string='Responsible vendor')
    contract_id = fields.Many2one('ethereum.contract.instance', string='Governing contract')

    @api.depends('belonging_ids')
    def _compute_hash(self):
        for o in self:
            h = hashlib.sha256()
            for b in o.belonging_ids:
                h.update(b.sha256)
            o.sha256 = h.hexdigest()

