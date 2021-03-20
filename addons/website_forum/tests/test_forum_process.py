# Part of Harpiya. See LICENSE file for full copyright and licensing details.

import harpiya.tests

@harpiya.tests.common.tagged('post_install', '-at_install')
class TestUi(harpiya.tests.HttpCase):

    def test_01_admin_forum_tour(self):
        self.start_tour("/", 'question', login="admin")

    def test_02_demo_question(self):
        forum = self.env.ref('website_forum.forum_help')
        demo = self.env.ref('base.user_demo')
        demo.karma = forum.karma_post + 1
        self.start_tour("/", 'forum_question', login="demo")
