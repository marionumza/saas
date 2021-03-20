# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.
from harpiya import fields, models
from harpiya.tools.translate import html_translate


class DigestTip(models.Model):
    _name = 'digest.tip'
    _description = 'Digest Tips'
    _order = 'sequence'

    sequence = fields.Integer(
        'Sequence', default=1,
        help='Used to display digest tip in email template base on order')
    user_ids = fields.Many2many(
        'res.users', string='Recipients',
        help='Users having already received this tip')
    tip_description = fields.Html('Tip description', translate=html_translate)
    group_id = fields.Many2one(
        'res.groups', string='Authorized Group',
        default=lambda self: self.env.ref('base.group_user'))
