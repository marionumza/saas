import harpiya.tests
from harpiya.tools import mute_logger


@harpiya.tests.common.tagged('post_install', '-at_install')
class TestWebsiteError(harpiya.tests.HttpCase):

    @mute_logger('harpiya.addons.http_routing.models.ir_http', 'harpiya.http')
    def test_01_run_test(self):
        self.start_tour("/test_error_view", 'test_error_website')
