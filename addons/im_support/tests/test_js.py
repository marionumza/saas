# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

import harpiya.tests


@harpiya.tests.tagged('post_install', '-at_install')
class IMSupportSuite(harpiya.tests.HttpCase):

    def test_im_support_js(self):
        self.phantom_js('/im_support/tests?mod=web&failfast', "", "", login='admin', timeout=180)
