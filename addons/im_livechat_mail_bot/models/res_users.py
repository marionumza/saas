# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import models, fields


class Users(models.Model):
    _inherit = 'res.users'
    harpiyabot_state = fields.Selection(
        selection_add=[
            ('onboarding_canned', 'Onboarding canned'),
        ])
