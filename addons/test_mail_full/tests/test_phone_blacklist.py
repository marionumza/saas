# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya.addons.sms.tests import common as sms_common
from harpiya.addons.test_mail_full.tests import common as test_mail_full_common


class TestPhoneBlacklist(test_mail_full_common.BaseFunctionalTest, sms_common.MockSMS, test_mail_full_common.TestRecipients):
    """ TODO """

    @classmethod
    def setUpClass(cls):
        super(TestPhoneBlacklist, cls).setUpClass()
        cls._test_body = 'VOID CONTENT'

        cls.test_record = cls.env['mail.test.sms.bl'].with_context(**cls._test_context).create({
            'name': 'Test',
            'customer_id': cls.partner_1.id,
            'mobile_nbr': cls.test_numbers[0],
            'phone_nbr': cls.test_numbers[1],
        })
        cls.test_record = cls._reset_mail_context(cls.test_record)

    def test_phone_blacklist_internals(self):
        with self.sudo('employee'):
            test_record = self.env['mail.test.sms.bl'].browse(self.test_record.id)
            self.assertEqual(test_record.phone_sanitized, self.test_numbers_san[1])
            self.assertFalse(test_record.phone_blacklisted)

            bl_record = self.env['phone.blacklist'].sudo().create([{'number': self.test_numbers_san[1]}])
            test_record.invalidate_cache()
            self.assertTrue(test_record.phone_blacklisted)

            self.env['phone.blacklist'].sudo().remove(self.test_numbers_san[1])
            self.assertFalse(bl_record.active)
            test_record.invalidate_cache()
            self.assertFalse(test_record.phone_blacklisted)

            self.env['phone.blacklist'].sudo().add(self.test_numbers_san[1])
            self.assertTrue(bl_record.active)
            test_record.invalidate_cache()
            self.assertTrue(test_record.phone_blacklisted)

            bl_record_2 = self.env['phone.blacklist'].sudo().create([{'number': self.test_numbers_san[1]}])
            self.assertEqual(bl_record, bl_record_2)

            rec = self.env['mail.test.sms.bl'].search([('phone_blacklisted', '=', True)])
            self.assertEqual(rec, test_record)

            bl_record.unlink()
            rec = self.env['mail.test.sms.bl'].search([('phone_blacklisted', '=', True)])
            self.assertEqual(rec, self.env['mail.test.sms.bl'])

    def test_phone_sanitize_api(self):
        with self.sudo('employee'):
            test_record = self.env['mail.test.sms.bl'].browse(self.test_record.id)
            self.assertFalse(test_record.phone_blacklisted)

            test_record._phone_set_blacklisted()
            test_record.invalidate_cache()
            self.assertTrue(test_record.phone_blacklisted)

            test_record._phone_reset_blacklisted()
            test_record.invalidate_cache()
            self.assertFalse(test_record.phone_blacklisted)

    def test_phone_sanitize_internals(self):
        with self.sudo('employee'):
            test_record = self.env['mail.test.sms.bl'].browse(self.test_record.id)
            self.assertEqual(test_record.phone_nbr, self.test_numbers[1])
            self.assertEqual(test_record.phone_sanitized, self.test_numbers_san[1])

            test_record.write({'phone_nbr': 'incorrect'})
            self.assertEqual(test_record.phone_nbr, 'incorrect')
            self.assertEqual(test_record.phone_sanitized, self.test_numbers_san[0])

            test_record.write({'mobile_nbr': 'incorrect'})
            self.assertEqual(test_record.mobile_nbr, 'incorrect')
            self.assertEqual(test_record.phone_sanitized, False)

            test_record.write({'phone_nbr': self.test_numbers[1]})
            self.assertEqual(test_record.phone_nbr, self.test_numbers[1])
            self.assertEqual(test_record.phone_sanitized, self.test_numbers_san[1])
