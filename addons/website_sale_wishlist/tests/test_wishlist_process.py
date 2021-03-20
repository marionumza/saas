# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.
import harpiya.tests


@harpiya.tests.common.at_install(False)
@harpiya.tests.common.post_install(True)
class TestUi(harpiya.tests.HttpCase):
    def test_01_wishlist_tour(self):
        self.start_tour("/", 'shop_wishlist')
