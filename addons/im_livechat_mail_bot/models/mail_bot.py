# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import models, _


class MailBot(models.AbstractModel):
    _inherit = 'mail.bot'

    def _get_answer(self, record, body, values, command):
        harpiyabot_state = self.env.user.harpiyabot_state
        if self._is_bot_in_private_channel(record):
            if harpiyabot_state == "onboarding_ping" and self._is_bot_pinged(values):
                self.env.user.harpiyabot_state = "onboarding_canned"
                return _("That's me! 🎉<br/>Try to type \":\" to use canned responses.")
            elif harpiyabot_state == "onboarding_canned" and values.get("canned_response_ids"):
                self.env.user.harpiyabot_state = "idle"
                return _("Good, you can customize canned responses in the live chat application.<br/><br/><b>It's the end of this overview</b>, enjoy discovering Harpiya!")
            #repeat question if needed
            elif harpiyabot_state == 'onboarding_canned':
                return _("Not sure wat you are doing. Please press : and wait for the propositions. Select one of them and press enter.")
        return super(MailBot, self)._get_answer(record, body, values, command)
