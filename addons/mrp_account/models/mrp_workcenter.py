# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import fields, models


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    costs_hour_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                            help="Fill this only if you want automatic analytic accounting entries on production orders.")
