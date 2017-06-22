from odoo import models, fields, api
from odoo.exceptions import ValidationError
import hashlib


CATEGORIES = [
    ('A1', 'Flat'),
    ('ST', 'Studio'),
    ('IR', 'Building'),
    ('COP', 'Coprop'),
    ('DX', 'Duplex'),
    ('M4', 'Isolated house'),
    ('M1+1', 'Twin house'),
    ('M2', 'Lined house'),
    ('CH1', 'Single room'),
    ('ENT', 'Deposit'),
    ('EMP', 'Free spot'),
    ('TR', 'Raw land')
]


class Belonging(models.Model):
    _name = 'casalta.belonging'

    name = fields.Char('Common name')
    ref = fields.Char('Internal reference')
    text = fields.Text('Description')
    contract_id = fields.Many2one('ethereum.contract.instance', string='Governing contract')
    sha256 = fields.Char('Validation tag', compute='_compute_hash', store=True)
    categ = fields.Selection(CATEGORIES, 'Category')
    offer = fields.Selection([
        ('buy', 'To buy'),
        ('rent', 'To rent'),
        ('viager', 'Viager')
    ], 'Offer')
    price = fields.Float('Price / Cost of renting')
    loc_caution = fields.Float('Amount for protection')
    loc_charges = fields.Float('Amount for charges')
    loc_furnished = fields.Boolean('With furnitures')
    peb = fields.Char('PEB description')
    state = fields.Selection([
        ('bad', 'To restore'),
        ('medium', 'Correct'),
        ('high', 'Nice')
    ], string='State')
    superficy = fields.Float('Superficy in square meters')
    partner_id = fields.Many2one('res.partner', string='Address')
    visit_ids = fields.Many2many('casalta.timeslot', string='Possible visits')
    offer_id = fields.Many2one('casalta.offer', string='Governing offer')
    date_in = fields.Date('Availability date')
    date_give = fields.Date('Giving out date')
    tax_price = fields.Float('Cadastral price')
    photo_ids = fields.One2many('casalta.photo', 'belonging_id', string='Photos')
    owner_ids = fields.One2many('casalta.owning', 'belonging_id', string='Owners')
    customer_ids = fields.One2many('casalta.owning', 'belonging_id', string='Interested people')

    @api.depends('categ', 'superficy', 'partner_id.street', 'partner_id.city', 'partner_id.country_id')
    def _compute_hash(self):
        for b in self:
            h = hashlib.sha256()
            h.update(str(b.categ))
            h.update(str(b.superficy))
            h.update(str(b.partner_id.street))
            h.update(str(b.partner_id.city))
            h.update(str(b.partner_id.country_id.name))
            b.sha256 = h.hexdigest()

