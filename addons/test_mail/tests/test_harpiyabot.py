# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from unittest.mock import patch

from harpiya.addons.test_mail.tests.common import BaseFunctionalTest, MockEmails, TestRecipients
from harpiya.tools import mute_logger
from harpiya.tests import tagged


@tagged("harpiyabot")
class TestHarpiyabot(BaseFunctionalTest, MockEmails, TestRecipients):

    @classmethod
    def setUpClass(cls):
        super(TestHarpiyabot, cls).setUpClass()
        cls.test_record = cls.env['mail.test.simple'].with_context(cls._test_context).create({'name': 'Test', 'email_from': 'ignasse@example.com'})

        cls.harpiyabot = cls.env.ref("base.partner_root")
        cls.message_post_default_kwargs = {
            'body': '',
            'attachment_ids': [],
            'message_type': 'comment',
            'partner_ids': [],
            'subtype': 'mail.mt_comment'
        }
        cls.harpiyabot_ping_body = '<a href="http://harpiya.com/web#model=res.partner&amp;id=%s" class="o_mail_redirect" data-oe-id="%s" data-oe-model="res.partner" target="_blank">@HarpiyaBot</a>' % (cls.harpiyabot.id, cls.harpiyabot.id)
        cls.test_record_employe = cls.test_record.with_user(cls.user_employee)

    @mute_logger('harpiya.addons.mail.models.mail_mail')
    def test_fetch_listener(self):
        channel = self.env['mail.channel'].with_user(self.user_employee).init_harpiyabot()
        partners = self.env['mail.channel'].channel_fetch_listeners(channel.uuid)
        harpiyabot = self.env.ref("base.partner_root")
        harpiyabot_in_fetch_listeners = [partner for partner in partners if partner['id'] == harpiyabot.id]
        self.assertEqual(len(harpiyabot_in_fetch_listeners), 1, 'harpiyabot should appear only once in channel_fetch_listeners')

    @mute_logger('harpiya.addons.mail.models.mail_mail')
    def test_harpiyabot_ping(self):
        kwargs = self.message_post_default_kwargs.copy()
        kwargs.update({'body': self.harpiyabot_ping_body, 'partner_ids': [self.harpiyabot.id, self.user_admin.partner_id.id]})

        with patch('random.choice', lambda x: x[0]):
            self.assertNextMessage(
                self.test_record_employe.with_context({'mail_post_autofollow': True}).message_post(**kwargs),
                sender=self.harpiyabot,
                answer=["Yep, HarpiyaBot is in the place!"]
            )
        # Harpiyabot should not be a follower but user_employee and user_admin should
        follower = self.test_record.message_follower_ids.mapped('partner_id')
        self.assertNotIn(self.harpiyabot, follower)
        self.assertIn(self.user_employee.partner_id, follower)
        self.assertIn(self.user_admin.partner_id, follower)

    @mute_logger('harpiya.addons.mail.models.mail_mail')
    def test_onboarding_flow(self):
        kwargs = self.message_post_default_kwargs.copy()
        channel = self.env['mail.channel'].with_user(self.user_employee).init_harpiyabot()

        kwargs['body'] = 'tagada 😊'
        self.assertNextMessage(
            channel.message_post(**kwargs),
            sender=self.harpiyabot,
            answer=("attachment",)
        )
        kwargs['body'] = ''
        attachment = self.env['ir.attachment'].with_user(self.user_employee).create({
            'datas': 'bWlncmF0aW9uIHRlc3Q=',
            'name': 'picture_of_your_dog.doc',
            'res_model': 'mail.compose.message',
        })
        kwargs['attachment_ids'] = [attachment.id]
        last_message = self.assertNextMessage(
            channel.message_post(**kwargs),
            sender=self.harpiyabot,
            answer=("help",)
        )
        kwargs['attachment_ids'] = []

        channel.execute_command(command="help")
        self.assertNextMessage(
            last_message,  # no message will be post with command help, use last harpiyabot message instead
            sender=self.harpiyabot,
            answer=("@HarpiyaBot",)
        )
        # we dont test the end of the flow since it will depends of the installed apps (livechat)
        self.user_employee.harpiyabot_state = "idle"
        kwargs['partner_ids'] = []
        kwargs['body'] = "I love you"
        self.assertNextMessage(
            channel.message_post(**kwargs),
            sender=self.harpiyabot,
            answer=("too human for me",)
        )
        kwargs['body'] = "Go fuck yourself"
        self.assertNextMessage(
            channel.message_post(**kwargs),
            sender=self.harpiyabot,
            answer=("I have feelings",)
        )

    @mute_logger('harpiya.addons.mail.models.mail_mail')
    def test_harpiyabot_no_default_answer(self):
        kwargs = self.message_post_default_kwargs.copy()
        kwargs.update({'body': "I'm not talking to @harpiyabot right now", 'partner_ids': []})
        self.assertNextMessage(
            self.test_record_employe.message_post(**kwargs),
            answer=False
        )

    def assertNextMessage(self, message, answer=None, sender=None):
        last_message = self.env['mail.message'].search([('id', '=', message.id + 1)])
        if last_message:
            body = last_message.body.replace('<p>', '').replace('</p>', '')
        else:
            self.assertFalse(answer, "No last message found when an answer was expect")
        if answer is not None:
            if answer and not last_message:
                self.assertTrue(False, "No last message found")
            if isinstance(answer, list):
                self.assertIn(body, answer)
            elif isinstance(answer, tuple):
                for elem in answer:
                    self.assertIn(elem, body)
            elif not answer:
                self.assertFalse(last_message, "No answer should have been post")
                return
            else:
                self.assertEqual(body, answer)
        if sender:
            self.assertEqual(sender, last_message.author_id)
        return last_message
