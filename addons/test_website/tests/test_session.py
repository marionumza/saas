import harpiya.tests
from harpiya.tools import mute_logger


@harpiya.tests.common.tagged('post_install', '-at_install')
class TestWebsiteSession(harpiya.tests.HttpCase):

    def test_01_run_test(self):
        self.start_tour('/', 'test_json_auth')
