# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.
from harpiya import api, models


class Partner(models.Model):
    _inherit = 'res.partner'

    def _compute_im_status(self):
        #we asume that mail_bot _compute_im_status will be executed after bus _compute_im_status
        super(Partner, self)._compute_im_status()
        harpiyabot_id = self.env['ir.model.data'].xmlid_to_res_id("base.partner_root")
        for partner in self:
            if partner.id == harpiyabot_id:
                partner.im_status = 'bot'

    @api.model
    def get_mention_suggestions(self, search, limit=8):
        #add harpiyabot in mention suggestion when pinging in mail_thread
        [users, partners] = super(Partner, self).get_mention_suggestions(search, limit=limit)
        if len(partners) + len(users) < limit and "harpiyabot".startswith(search.lower()):
            harpiyabot = self.env.ref("base.partner_root")
            if not any([elem['id'] == harpiyabot.id for elem in partners]):
                if harpiyabot:
                    partners.append({'id': harpiyabot.id, 'name': harpiyabot.name, 'email': harpiyabot.email})
        return [users, partners]

