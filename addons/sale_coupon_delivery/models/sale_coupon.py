# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.


from harpiya import models, _


class SaleCoupon(models.Model):
    _inherit = "sale.coupon"

    def _check_coupon_code(self, order):
        if self.program_id.reward_type == 'free_shipping' and not order.order_line.filtered(lambda line: line.is_delivery):
            return {'error': _('The shipping costs are not in the order lines.')}
        return super(SaleCoupon, self)._check_coupon_code(order)
