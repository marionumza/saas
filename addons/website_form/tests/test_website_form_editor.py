# Part of Harpiya. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-

import harpiya.tests


@harpiya.tests.tagged('post_install','-at_install')
class TestWebsiteFormEditor(harpiya.tests.HttpCase):
    def test_tour(self):
        self.start_tour("/", 'website_form_editor_tour', login="admin")
        self.start_tour("/", 'website_form_editor_tour_submit')
        self.start_tour("/", 'website_form_editor_tour_results', login="admin")
