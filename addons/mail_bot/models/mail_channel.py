# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import api, models, _


class Channel(models.Model):
    _inherit = 'mail.channel'

    def _execute_command_help(self, **kwargs):
        super(Channel, self)._execute_command_help(**kwargs)
        self.env['mail.bot']._apply_logic(self, kwargs, command="help")  # kwargs are not usefull but...

    @api.model
    def init_harpiyabot(self):
        if self.env.user.harpiyabot_state == 'not_initialized':
            partner = self.env.user.partner_id
            harpiyabot_id = self.env['ir.model.data'].xmlid_to_res_id("base.partner_root")
            channel = self.with_context(mail_create_nosubscribe=True).create({
                'channel_partner_ids': [(4, partner.id), (4, harpiyabot_id)],
                'public': 'private',
                'channel_type': 'chat',
                'email_send': False,
                'name': 'HarpiyaBot'
            })
            message = _("Hello,<br/>Harpiya's chat helps employees collaborate efficiently. I'm here to help you discover its features.<br/><b>Try to send me an emoji :)</b>")
            channel.sudo().message_post(body=message, author_id=harpiyabot_id, message_type="comment", subtype="mail.mt_comment")
            self.env.user.harpiyabot_state = 'onboarding_emoji'
            return channel
