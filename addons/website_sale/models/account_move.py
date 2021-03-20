# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    website_id = fields.Many2one('website', related='partner_id.website_id', string='Website',
                                 help='Website through which this invoice was created.',
                                 store=True, readonly=True, tracking=True)
