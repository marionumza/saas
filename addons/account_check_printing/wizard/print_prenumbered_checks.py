# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

import re
from harpiya import api, fields, models, _
from harpiya.exceptions import ValidationError


class PrintPreNumberedChecks(models.TransientModel):
    _name = 'print.prenumbered.checks'
    _description = 'Print Pre-numbered Checks'

    next_check_number = fields.Char('Next Check Number', required=True)

    @api.constrains('next_check_number')
    def _check_next_check_number(self):
        for check in self:
            if check.next_check_number and not re.match(r'^[0-9]+$', check.next_check_number):
                raise ValidationError(_('Next Check Number should only contains numbers.'))

    def print_checks(self):
        check_number = int(self.next_check_number)
        payments = self.env['account.payment'].browse(self.env.context['payment_ids'])
        payments.filtered(lambda r: r.state == 'draft').post()
        payments.filtered(lambda r: r.state not in ('sent', 'cancelled')).write({'state': 'sent'})
        for payment in payments:
            payment.check_number = check_number
            check_number += 1
        return payments.do_print_checks()
