import harpiya.tests
# Part of Harpiya. See LICENSE file for full copyright and licensing details.


@harpiya.tests.tagged('post_install', '-at_install')
class TestUi(harpiya.tests.HttpCase):
    def test_01_event_configurator(self):
        self.start_tour("/web", 'event_configurator_tour', login="admin")
