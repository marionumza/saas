# Part of Harpiya. See LICENSE file for full copyright and licensing details.
import harpiya.tests


@harpiya.tests.common.tagged('post_install', '-at_install')
class TestWebsiteControllerArgs(harpiya.tests.HttpCase):

    def test_crawl_args(self):
        req = self.url_open('/ignore_args/converter/valueA/?b=valueB&c=valueC')
        self.assertEquals(req.status_code, 200)
        self.assertEquals(req.json(), {'a': 'valueA', 'b': 'valueB', 'kw': {'c': 'valueC'}})

        req = self.url_open('/ignore_args/converter/valueA/nokw?b=valueB&c=valueC')
        self.assertEquals(req.status_code, 200)
        self.assertEquals(req.json(), {'a': 'valueA', 'b': 'valueB'})

        req = self.url_open('/ignore_args/converteronly/valueA/?b=valueB&c=valueC')
        self.assertEquals(req.status_code, 200)
        self.assertEquals(req.json(), {'a': 'valueA', 'kw': None})

        req = self.url_open('/ignore_args/none?a=valueA&b=valueB')
        self.assertEquals(req.status_code, 200)
        self.assertEquals(req.json(), {'a': None, 'kw': None})

        req = self.url_open('/ignore_args/a?a=valueA&b=valueB')
        self.assertEquals(req.status_code, 200)
        self.assertEquals(req.json(), {'a': 'valueA', 'kw': None})

        req = self.url_open('/ignore_args/kw?a=valueA&b=valueB')
        self.assertEquals(req.status_code, 200)
        self.assertEquals(req.json(), {'a': 'valueA', 'kw': {'b': 'valueB'}})
