# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import http
from harpiya.http import request
from harpiya.addons.http_routing.models.ir_http import unslug
from harpiya.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    @http.route(["/sale_quotation_builder/template/<string:template_id>"], type='http', auth="user", website=True)
    def sale_quotation_builder_template_view(self, template_id, **post):
        template_id = unslug(template_id)[-1]
        template = request.env['sale.order.template'].browse(template_id).with_context(
            allowed_company_ids=request.env.user.company_ids.ids,
        )
        values = {'template': template}
        return request.render('sale_quotation_builder.so_template', values)
