import harpiya.tests


@harpiya.tests.tagged('post_install', '-at_install')
class TestUi(harpiya.tests.HttpCase):
    def test_admin(self):
        self.start_tour("/", 'event', login='admin')
