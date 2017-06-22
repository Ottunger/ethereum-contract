from odoo import models, fields, api
from odoo.exceptions import ValidationError
import hashlib
from datetime import datetime


class Offer(models.Model):
    _name = 'casalta.offer'

    sha256 = fields.Char('Validation tag', compute='_compute_hash', store=True)
    contract_value = fields.Float('Underlying value', compute='_compute_hash', store=True)
    belonging_ids = fields.One2many('casalta.belonging', 'offer_id', string='Offers')
    user_id = fields.Many2one('res.users', string='Responsible vendor')
    price = fields.Float('Price for processing offer')
    state = fields.Selection([
        ('open', 'In edit'),
        ('pending', 'Pending signatures'),
        ('signed', 'Signed')
    ], 'State', readonly=True, default='open')
    contract_id = fields.Many2one('ethereum.contract.instance', string='Governing contract', readonly=True)
    date_from = fields.Date('Mandated from')
    date_to = fields.Date('Mandated to')
    attachment_ids = fields.One2many('casalta.photo', 'offer_id', string='Attachments')

    @api.multi
    def write(self, vals):
        if self.state != 'open':
            if vals.get('belonging_ids', False) or vals.get('date_from', False) or vals.get('date_to', False) or vals.get('attachment_ids', False) or vals.get('price', False):
                raise ValidationError('Cannot modify signed values after agreement')
        return super(Offer, self).write(vals)

    @api.depends('belonging_ids', 'date_from', 'date_to', 'attachment_ids', 'price')
    def _compute_hash(self):
        for o in self:
            value = 0.0
            h = hashlib.sha256()
            h.update(str(o.date_from))
            h.update(str(o.date_to))
            for b in o.belonging_ids:
                value += b.price
                h.update(str(b.sha256))
            for a in o.attachment_ids:
                h.update(str(a.contained))
            h.update(str(value))
            h.update(str(o.price))
            o.contract_value = value
            o.sha256 = h.hexdigest()

    @api.one
    def action_pending(self):
        self.ensure_one()
        if self.state != 'open':
            raise ValidationError('Can only be called when state is open')
        contract = request.env['ethereum.contract'].search([('type', '=', 'sell_mandate')])
        if len(contract) == 0:
            raise ValidationError('No contract matching type defined')
        website = request.env['website'].browse(1)
        resp = website.sm_new(contract[0], [
            False,
            website.eth_account,
            datetime.strptime(self.date_from, '%Y-%m-%d').timestamp(),
            datetime.strptime(self.date_to, '%Y-%m-%d').timestamp(),
            self.sha256,
            self.price,
            self.contract_value
        ])[0][0]
        if resp.get('address', None) is not None:
            new_instance_id = request.env['ethereum.contract.instance'].create({
                'contract_id': contract.id,
                'addr': resp['address']
            })
            self.write({
                'contract_id': new_instance_id,
                'state': 'pending' 
            })
        return False

    @api.one
    def action_sign(self):
        self.ensure_one()
        if state != 'pending':
            raise ValidationError('This contract must be written before signing')
        website = request.env['website'].browse(1)
        resp = website.sm_sign(self.contract_id)[0][0]
        if resp.get('transactionHash', None) is not None:
            resp = website.sm_get(self.contract_id)[0][0]
            if resp[10] is False:
                self.state = 'signed'
        return False

