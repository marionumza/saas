# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from psycopg2 import IntegrityError

from harpiya.tests import tagged
from harpiya.addons.test_mail.tests import common
from harpiya.tools.misc import mute_logger


class BaseFollowersTest(common.BaseFunctionalTest):

    @classmethod
    def setUpClass(cls):
        super(BaseFollowersTest, cls).setUpClass()
        cls.test_record = cls.env['mail.test.simple'].with_context(cls._test_context).create({'name': 'Test', 'email_from': 'ignasse@example.com'})
        cls._create_portal_user()
        cls._create_channel_listener()

        Subtype = cls.env['mail.message.subtype']
        cls.mt_mg_def = Subtype.create({'name': 'mt_mg_def', 'default': True, 'res_model': 'mail.test.simple'})
        cls.mt_cl_def = Subtype.create({'name': 'mt_cl_def', 'default': True, 'res_model': 'mail.test'})
        cls.mt_al_def = Subtype.create({'name': 'mt_al_def', 'default': True, 'res_model': False})
        cls.mt_mg_nodef = Subtype.create({'name': 'mt_mg_nodef', 'default': False, 'res_model': 'mail.test.simple'})
        cls.mt_al_nodef = Subtype.create({'name': 'mt_al_nodef', 'default': False, 'res_model': False})
        cls.mt_mg_def_int = cls.env['mail.message.subtype'].create({'name': 'mt_mg_def', 'default': True, 'res_model': 'mail.test.simple', 'internal': True})
        cls.default_group_subtypes = Subtype.search([('default', '=', True), '|', ('res_model', '=', 'mail.test.simple'), ('res_model', '=', False)])
        cls.default_group_subtypes_portal = Subtype.search([('internal', '=', False), ('default', '=', True), '|', ('res_model', '=', 'mail.test.simple'), ('res_model', '=', False)])

    def test_field_message_is_follower(self):
        test_record = self.test_record.with_user(self.user_employee)
        followed_before = test_record.search([('message_is_follower', '=', True)])
        self.assertFalse(test_record.message_is_follower)
        test_record.message_subscribe(partner_ids=[self.user_employee.partner_id.id])
        followed_after = test_record.search([('message_is_follower', '=', True)])
        self.assertTrue(test_record.message_is_follower)
        self.assertEqual(followed_before | test_record, followed_after)

    def test_field_followers(self):
        test_record = self.test_record.with_user(self.user_employee)
        test_record.message_subscribe(partner_ids=[self.user_employee.partner_id.id, self.user_admin.partner_id.id], channel_ids=[self.channel_listen.id])
        followers = self.env['mail.followers'].search([
            ('res_model', '=', 'mail.test.simple'),
            ('res_id', '=', test_record.id)])
        self.assertEqual(followers, test_record.message_follower_ids)
        self.assertEqual(test_record.message_partner_ids, self.user_employee.partner_id | self.user_admin.partner_id)
        self.assertEqual(test_record.message_channel_ids, self.channel_listen)

    def test_followers_subtypes_default(self):
        test_record = self.test_record.with_user(self.user_employee)
        test_record.message_subscribe(partner_ids=[self.user_employee.partner_id.id])
        self.assertEqual(test_record.message_partner_ids, self.user_employee.partner_id)
        follower = self.env['mail.followers'].search([
            ('res_model', '=', 'mail.test.simple'),
            ('res_id', '=', test_record.id),
            ('partner_id', '=', self.user_employee.partner_id.id)])
        self.assertEqual(follower, test_record.message_follower_ids)
        self.assertEqual(follower.subtype_ids, self.default_group_subtypes)

    def test_followers_subtypes_default_internal(self):
        test_record = self.test_record.with_user(self.user_employee)
        test_record.message_subscribe(partner_ids=[self.partner_portal.id])
        self.assertEqual(test_record.message_partner_ids, self.partner_portal)
        follower = self.env['mail.followers'].search([
            ('res_model', '=', 'mail.test.simple'),
            ('res_id', '=', test_record.id),
            ('partner_id', '=', self.partner_portal.id)])
        self.assertEqual(follower.subtype_ids, self.default_group_subtypes_portal)

    def test_followers_subtypes_specified(self):
        test_record = self.test_record.with_user(self.user_employee)
        test_record.message_subscribe(partner_ids=[self.user_employee.partner_id.id], subtype_ids=[self.mt_mg_nodef.id])
        self.assertEqual(test_record.message_partner_ids, self.user_employee.partner_id)
        follower = self.env['mail.followers'].search([
            ('res_model', '=', 'mail.test.simple'),
            ('res_id', '=', test_record.id),
            ('partner_id', '=', self.user_employee.partner_id.id)])
        self.assertEqual(follower, test_record.message_follower_ids)
        self.assertEqual(follower.subtype_ids, self.mt_mg_nodef)

    def test_followers_multiple_subscription_force(self):
        test_record = self.test_record.with_user(self.user_employee)

        test_record.message_subscribe(partner_ids=[self.user_admin.partner_id.id], subtype_ids=[self.mt_mg_nodef.id])
        self.assertEqual(test_record.message_partner_ids, self.user_admin.partner_id)
        self.assertEqual(test_record.message_channel_ids, self.env['mail.channel'])
        self.assertEqual(test_record.message_follower_ids.subtype_ids, self.mt_mg_nodef)

        test_record.message_subscribe(partner_ids=[self.user_admin.partner_id.id], subtype_ids=[self.mt_mg_nodef.id, self.mt_al_nodef.id])
        self.assertEqual(test_record.message_partner_ids, self.user_admin.partner_id)
        self.assertEqual(test_record.message_channel_ids, self.env['mail.channel'])
        self.assertEqual(test_record.message_follower_ids.subtype_ids, self.mt_mg_nodef | self.mt_al_nodef)

    def test_followers_multiple_subscription_noforce(self):
        test_record = self.test_record.with_user(self.user_employee)

        test_record.message_subscribe(partner_ids=[self.user_admin.partner_id.id], subtype_ids=[self.mt_mg_nodef.id, self.mt_al_nodef.id])
        self.assertEqual(test_record.message_partner_ids, self.user_admin.partner_id)
        self.assertEqual(test_record.message_channel_ids, self.env['mail.channel'])
        self.assertEqual(test_record.message_follower_ids.subtype_ids, self.mt_mg_nodef | self.mt_al_nodef)

        # set new subtypes with force=False, meaning no rewriting of the subscription is done -> result should not change
        test_record.message_subscribe(partner_ids=[self.user_admin.partner_id.id])
        self.assertEqual(test_record.message_partner_ids, self.user_admin.partner_id)
        self.assertEqual(test_record.message_channel_ids, self.env['mail.channel'])
        self.assertEqual(test_record.message_follower_ids.subtype_ids, self.mt_mg_nodef | self.mt_al_nodef)

    def test_followers_no_DID(self):
        """Test that a follower cannot suffer from dissociative identity disorder.
           It cannot be both a partner and a channel.
        """
        with self.assertRaises(IntegrityError), mute_logger('harpiya.sql_db'):
            self.env['mail.followers'].create({
                'res_model': self.test_record._name,
                'res_id': self.test_record.id,
                'partner_id': self.user_employee.partner_id.id,
                'channel_id': self.channel_listen.id,
            })

    def test_followers_default_partner_context(self):
        """Test that a follower partner_id is not taken from context
           when channel id is also defined.
        """
        test_record = self.test_record.with_user(self.user_employee)
        test_record.with_context(default_partner_id=1).message_subscribe(
            partner_ids=[self.user_employee.partner_id.id, self.user_admin.partner_id.id],
            channel_ids=[self.channel_listen.id]
        )


class AdvancedFollowersTest(common.BaseFunctionalTest):
    @classmethod
    def setUpClass(cls):
        super(AdvancedFollowersTest, cls).setUpClass()
        cls._create_portal_user()

        cls.test_track = cls.env['mail.test.track'].with_user(cls.user_employee).create({
            'name': 'Test',
        })

        Subtype = cls.env['mail.message.subtype']

        # clean demo data to avoid interferences
        Subtype.search([('res_model', 'in', ['mail.test', 'mail.test.track'])]).unlink()

        cls.sub_nodef = Subtype.create({'name': 'Sub NoDefault', 'default': False, 'res_model': 'mail.test'})
        cls.sub_umb1 = Subtype.create({'name': 'Sub Umbrella1', 'default': False, 'res_model': 'mail.test.track'})
        cls.sub_umb2 = Subtype.create({'name': 'Sub Umbrella2', 'default': False, 'res_model': 'mail.test.track'})
        cls.umb_def = Subtype.create({'name': 'Umbrella Default', 'default': True, 'res_model': 'mail.test'})
        # create subtypes for auto subscription from umbrella to sub records
        cls.umb_sub_def = Subtype.create({
            'name': 'Umbrella Sub1', 'default': True, 'res_model': 'mail.test',
            'parent_id': cls.sub_umb1.id, 'relation_field': 'umbrella_id'})
        cls.umb_sub_nodef = Subtype.create({
            'name': 'Umbrella Sub2', 'default': False, 'res_model': 'mail.test',
            'parent_id': cls.sub_umb2.id, 'relation_field': 'umbrella_id'})

    def test_auto_subscribe_create(self):
        """ Creator of records are automatically added as followers """
        self.assertEqual(self.test_track.message_partner_ids, self.user_employee.partner_id)

    def test_auto_subscribe_post(self):
        """ People posting a message are automatically added as followers """
        self.test_track.with_user(self.user_admin).message_post(body='Coucou hibou', message_type='comment')
        self.assertEqual(self.test_track.message_partner_ids, self.user_employee.partner_id | self.user_admin.partner_id)

    def test_auto_subscribe_post_email(self):
        """ People posting an email are automatically added as followers """
        self.test_track.with_user(self.user_admin).message_post(body='Coucou hibou', message_type='email')
        self.assertEqual(self.test_track.message_partner_ids, self.user_employee.partner_id | self.user_admin.partner_id)

    def test_auto_subscribe_not_on_notification(self):
        """ People posting an automatic notification are not subscribed """
        self.test_track.with_user(self.user_admin).message_post(body='Coucou hibou', message_type='notification')
        self.assertEqual(self.test_track.message_partner_ids, self.user_employee.partner_id)

    def test_auto_subscribe_responsible(self):
        """ Responsibles are tracked and added as followers """
        sub = self.env['mail.test.track'].with_user(self.user_employee).create({
            'name': 'Test',
            'user_id': self.user_admin.id,
        })
        self.assertEqual(sub.message_partner_ids, (self.user_employee.partner_id | self.user_admin.partner_id))

    def test_auto_subscribe_defaults(self):
        """ Test auto subscription based on an umbrella record. This mimics
        the behavior of addons like project and task where subscribing to
        some project's subtypes automatically subscribe the follower to its tasks.

        Functional rules applied here

         * subscribing to an umbrella subtype with parent_id / relation_field set
           automatically create subscription with matching subtypes
         * subscribing to a sub-record as creator applies default subtype values
         * portal user should not have access to internal subtypes
        """
        umbrella = self.env['mail.test'].with_context(self._test_context).create({
            'name': 'Project-Like',
        })

        umbrella.message_subscribe(partner_ids=[self.partner_portal.id])
        self.assertEqual(umbrella.message_partner_ids, self.partner_portal)

        sub1 = self.env['mail.test.track'].with_user(self.user_employee).create({
            'name': 'Task-Like Test',
            'umbrella_id': umbrella.id,
        })

        all_defaults = self.env['mail.message.subtype'].search([('default', '=', True), '|', ('res_model', '=', 'mail.test.track'), ('res_model', '=', False)])
        external_defaults = all_defaults.filtered(lambda subtype: not subtype.internal)

        self.assertEqual(sub1.message_partner_ids, self.partner_portal | self.user_employee.partner_id)
        self.assertEqual(
            sub1.message_follower_ids.filtered(lambda fol: fol.partner_id == self.partner_portal).subtype_ids,
            external_defaults | self.sub_umb1)
        self.assertEqual(
            sub1.message_follower_ids.filtered(lambda fol: fol.partner_id == self.user_employee.partner_id).subtype_ids,
            all_defaults)


@tagged('post_install', '-at_install')
class DuplicateNotificationTest(common.BaseFunctionalTest):
    def test_no_duplicate_notification(self):
        """
        Check that we only create one mail.notification per partner

        Post install because we need the registery to be ready to send notification
        """
        #Simulate case of 2 users that got their partner merged
        common_partner = self.env['res.partner'].create({"name": "demo1", "email": "demo1@test.com"})
        user_1 = self.env['res.users'].create({'login': 'demo1', 'partner_id': common_partner.id, 'notification_type': 'email'})
        user_2 = self.env['res.users'].create({'login': 'demo2', 'partner_id': common_partner.id, 'notification_type': 'inbox'})

        #Trigger auto subscribe notification
        test = self.env['mail.test.track'].create({"name": "Test Track", "user_id": user_2.id})
        mail_message = self.env['mail.message'].search([
             ('res_id', '=', test.id),
             ('model', '=', 'mail.test.track'),
             ('message_type', '=', 'user_notification')
        ])
        notif = self.env['mail.notification'].search([
            ('mail_message_id', '=', mail_message.id),
            ('res_partner_id', '=', common_partner.id)
        ])
        self.assertEqual(len(notif), 1)
        self.assertEqual(notif.notification_type, 'email')

        subtype = self.env.ref('mail.mt_comment')
        res = self.env['mail.followers']._get_recipient_data(test, 'comment',  subtype.id, pids=common_partner.ids)
        partner_notif = [r for r in res if r[0] == common_partner.id]
        self.assertEqual(len(partner_notif), 1)
        self.assertEqual(partner_notif[0][5], 'email')

@tagged('post_install', '-at_install')
class UnlinkedNotificationTest(common.BaseFunctionalTest):
    def test_unlinked_notification(self):
        """
        Check that we unlink the created user_notification after unlinked the related document

        Post install because we need the registery to be ready to send notification
        """
        common_partner = self.env['res.partner'].create({"name": "demo1", "email": "demo1@test.com"})
        user_1 = self.env['res.users'].create({'login': 'demo1', 'partner_id': common_partner.id, 'notification_type': 'inbox'})

        test = self.env['mail.test.track'].create({"name": "Test Track", "user_id": user_1.id})
        test_id = test.id
        mail_message = self.env['mail.message'].search([
             ('res_id', '=', test_id),
             ('model', '=', 'mail.test.track'),
             ('message_type', '=', 'user_notification')
        ])
        self.assertEqual(len(mail_message), 1)
        test.unlink()
        mail_message = self.env['mail.message'].search([
             ('res_id', '=', test_id),
             ('model', '=', 'mail.test.track'),
             ('message_type', '=', 'user_notification')
        ])
        self.assertEqual(len(mail_message), 0)
