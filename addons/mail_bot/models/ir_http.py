# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import models


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(Http, self).session_info()
        if self.env.user.has_group('base.group_user'):
            res['harpiyabot_initialized'] = self.env.user.harpiyabot_state != 'not_initialized'
        return res
