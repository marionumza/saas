import werkzeug

from harpiya import http
from harpiya.http import request

from harpiya.addons.http_routing.models.ir_http import slug
from harpiya.addons.website.models.ir_http import sitemap_qs2dom
from harpiya.addons.website_sale.controllers.main import WebsiteSale


def sitemap_shop(env, rule, qs):
    if not qs or qs.lower() in '/shop':
        yield {'loc': '/shop'}

    Category = env['product.public.category']
    dom = sitemap_qs2dom(qs, '/shop/category', Category._rec_name)
    dom += env['website'].get_current_website().website_domain()
    for cat in Category.search(dom):
        loc = '/shop/category/%s' % slug(cat)
        if not qs or qs.lower() in loc:
            yield {'loc': loc}


class WebsiteSaleWholesale(WebsiteSale):
    @http.route(auth="public", type='http')
    def shop(self, **post):
        Website = request.env['website'].get_current_website()
        if Website.wholesale and not request.session.uid:
            return werkzeug.utils.redirect('/web/login', 303)
        else:
            return super(WebsiteSaleWholesale, self).shop(**post)

    @http.route(auth="public")
    def product(self, product, category='', search='', **kwargs):
        Website = request.env['website'].get_current_website()
        if Website.wholesale and not request.session.uid:
            return werkzeug.utils.redirect('/web/login', 303)
        else:
            return super(WebsiteSaleWholesale, self).product(product, **kwargs)
