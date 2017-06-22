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
    state = fields.Selection([
        ('open', 'In edit'),
        ('running', 'Written'),
        ('tobuy', 'Validated'),
        ('bought', 'Bought by Casalta')
    ], 'State', readonly=True, default='open')
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
    status = fields.Selection([
        ('bad', 'To restore'),
        ('medium', 'Correct'),
        ('high', 'Nice')
    ], string='State')
    superficy = fields.Float('Superficy in square meters')
    street = fields.Char('Street line 1')
    street2 = fields.Char('Street line 2')
    zipcode = fields.Char('Zip code')
    city = fields.Char('City')
    country_id = fields.Many2one('res.country', string='Country')
    visit_ids = fields.Many2many('casalta.timeslot', string='Possible visits')
    offer_id = fields.Many2one('casalta.offer', string='Governing offer')
    date_in = fields.Date('Availability date')
    date_give = fields.Date('Giving out date')
    tax_price = fields.Float('Cadastral price')
    photo_ids = fields.One2many('casalta.photo', 'belonging_id', string='Photos')
    attachment_ids = fields.One2many('casalta.photo', 'belonging_id', string='Attachments')
    owner_ids = fields.One2many('casalta.owning', 'belonging_id', string='Owners')
    customer_ids = fields.One2many('casalta.owning', 'belonging_id', string='Interested people')

    @api.multi
    def write(self, vals):
        if self.state != 'open' or (self.contract_id and self.contract_id.state != 'open'):
            if vals.get('categ', False) or vals.get('superficy', False) or vals.get('street', False) or vals.get('street2', False) or vals.get('zipcode', False) or vals.get('city', False) or vals.get('country_id', False):
                raise ValidationError('Cannot modify signed values after agreement')
        return super(Offer, self).write(vals)

    @api.depends('categ', 'superficy', 'street', 'street2', 'zipcode', 'city', 'country_id')
    def _compute_hash(self):
        for b in self:
            h = hashlib.sha256()
            h.update(str(b.categ))
            h.update(str(b.superficy))
            h.update(str(b.street))
            h.update(str(b.street2))
            h.update(str(b.zipcode))
            h.update(str(b.city))
            h.update(str(b.country_id.name))
            b.sha256 = h.hexdigest()

    @api.one
    def action_pending(self):
        self.ensure_one()
        if self.state != 'open':
            raise ValidationError('Can only be called when state is open')
        distri = 0.0
        for o in self.owner_ids:
            distri += o.share
            if o.share < 0.1:
                raise ValidationError('A share percentage cannot be negative')
        if ditri < 99.9 or distri > 100.1:
            raise ValidationError('The share are not given around 100.0%')

        contract = request.env['ethereum.contract'].search([('type', '=', 'split_sell')])
        if len(contract) == 0:
            raise ValidationError('No contract matching type defined')
        website = request.env['website'].browse(1)
        resp = website.ss_new(contract[0], [
            self.price,
            self.sha256
        ])[0][0]
        if resp.get('address', None) is not None:
            new_instance_id = request.env['ethereum.contract.instance'].create({
                'contract_id': contract.id,
                'addr': resp['address']
            })
            self.write({
                'contract_id': new_instance_id,
                'state': 'running' 
            })
            #Now we distribute the shares, at our expense
            new_instance = self.env['ethereum.contract.instance'].browse(new_instance_id)
            for o in owner_ids:
                website.ss_addAuth(new_instance, [o.share * self.price, o.user_id.eth_account])
        return False

    @api.one
    def action_reclaim(self):
        self.ensure_one()
        if self.state != 'running':
            raise ValidationError('Can only reclaim during written phase')
        for o in self.owner_ids:
            if o.user_id.id == self.env.user.id:
                resp = website.ss_buyShare(self.contract_id, [
                    o.share * self.price,
                    o.user_id.name,
                    o.user_id.rrn
                ])[0][0]
                if resp.get('transactionHash', None) is not None:
                    resp = website.ss_get(self.contract_id)[0][0]
                if resp[5] is True:
                    self.state = 'tobuy'

    @api.one
    def action_buy(self):
        self.ensure_one()
        if self.state != 'tobuy':
            raise ValidationError('Can only buy if reclaimed')
        self.state = 'bought'

