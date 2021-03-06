# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.
from harpiya import api, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _has_unsplash_key_rights(self):
        self.ensure_one()
        return self.has_group('base.group_erp_manager')
