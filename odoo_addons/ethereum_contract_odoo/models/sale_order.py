from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        user = self.env['res.users'].search([('partner_id', '=', self.partner_id.id)])
        if user:
            for line in self.order_line:
                if line.product_id.worth_ether > 0.0:
                    self.env['website'].browse(1).mine_for_ether(user.eth_account, user.eth_password, 1000000000 * line.product_id.worth_ether * line.product_uom_qty)
        return super(SaleOrder, self).action_confirm()

