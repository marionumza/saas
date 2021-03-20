# coding: utf-8
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import fields, models


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    def _get_payment_terminal_selection(self):
        return super(PosPaymentMethod, self)._get_payment_terminal_selection() + [('six_tim', 'SIX without IoT Box')]

    six_terminal_ip = fields.Char('Six Terminal IP')
