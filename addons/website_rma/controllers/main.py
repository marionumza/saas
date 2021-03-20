# -*- coding: utf-8 -*-

from harpiya import SUPERUSER_ID, http, tools, _
from harpiya.http import request
from datetime import datetime
from harpiya.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from harpiya.exceptions import UserError


class website_rma(CustomerPortal):

    def _prepare_portal_layout_values(self):
        """ Add sales documents to main account page """
        values = super(website_rma, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        SaleOrder = request.env['sale.order']
        Invoice = request.env['account.move']
        Rma = request.env['rma.order']

        quotation_count = SaleOrder.search_count([
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['sent', 'cancel'])
        ])
        order_count = SaleOrder.search_count([
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['sale', 'done'])
        ])
        invoice_count = Invoice.search_count([
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['draft', 'posted', 'cancelled'])
        ])

        rma_count = Rma.search_count([
            ('partner_id', '=', int(partner.id)),
            ('state', 'in', ['draft', 'confirmed', 'approved', 'return'])
        ])
        values.update({
            'quotation_count': quotation_count,
            'order_count': order_count,
            'invoice_count': invoice_count,
            'rma_count': rma_count,
        })
        return values

    @http.route(['/my/rma', '/my/rma/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_rma(self, page=1, date_begin=None, date_end=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        RmaOrder = request.env['rma.order']

        domain = [('partner_id', '=', partner.id), ('state', 'in', ['draft', 'confirmed', 'approved', 'return'])]

        archive_groups = self._get_archive_groups('rma.order', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        rma_count = RmaOrder.search_count(domain)
        # pager
        pager = request.website.pager(
            url="/my/rma",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=rma_count,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        rma = RmaOrder.search(domain, limit=self._items_per_page, offset=pager['offset'])
        values.update({
            'date': date_begin,
            'rma': rma,
            'page_name': 'rma',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/rma',
        })
        return request.render("website_rma.portal_my_rma", values)


class HarpiyaWebsiteRMA(http.Controller):

    @http.route(['/rma/thankyou'], type='http', auth="public", website=True)
    def website_rma(self, **post):

        partner_id = post['partner_id']
        order_id = post['order_id']
        product_id = post['product_id']
        quantity = post['quantity']
        reason = post['reason']

        rma_order_obj = request.env['rma.order']
        product_obj = request.env['product.product']
        sale_order_obj = request.env['sale.order']
        stock_picking_obj = request.env['stock.picking'].sudo()

        sale_order = sale_order_obj.sudo().browse(int(order_id))
        product_data = product_obj.sudo().browse(int(product_id))

        vals = {'partner_id': partner_id, 'order_id': order_id, 'rma_product_id': product_id,
                'rma_product_uom_qty': quantity, 'reason': reason, 'rma_product_uom': product_data.uom_id.id,
                'user_id': sale_order.user_id.id, 'team_id': sale_order.team_id.id,
                'company_id': sale_order.company_id.id}

        rma_order_create = rma_order_obj.sudo().create(vals)

        for picking in sale_order.picking_ids:
            return_picking_obj = request.env['stock.return.picking']
            picking_obj = request.env['stock.picking'].sudo().browse(picking)
            stock_move_ids = request.env['stock.move'].sudo().search([('picking_id', '=', picking.id)])

            for return_move in stock_move_ids:
                return_move.move_dest_ids.filtered(lambda m: m.state not in ('done', 'cancel'))._do_unreserve()

            picking_type_id = picking.picking_type_id.return_picking_type_id.id or picking.picking_type_id.id
            new_picking = picking.copy({
                'move_lines': [],
                'picking_type_id': picking_type_id,
                'state': 'draft',
                'origin': _("Return of %s") % picking.name,
                'location_id': picking.location_dest_id.id,
                'location_dest_id': picking.location_id.id})
            new_picking.message_post_with_view('mail.message_origin_link',
                                               values={'self': new_picking, 'origin': picking},
                                               subtype_id=request.env.ref('mail.mt_note').id)
            returned_lines = 0

            for return_line in stock_move_ids:
                if not return_line:
                    raise UserError(_("You have manually created product lines, please delete them to proceed"))
                # TODO sle: float_is_zero?
                if quantity:
                    returned_lines += 1
                    # vals = return_picking_obj._prepare_move_default_values(return_line, new_picking)
                    vals = {
                        'product_id': return_line.product_id.id,
                        'product_uom_qty': quantity,
                        'picking_id': new_picking.id,
                        'state': 'draft',
                        'location_id': return_line.location_dest_id.id,
                        'location_dest_id': picking.location_id.id or return_line.location_id.id,
                        'picking_type_id': new_picking.picking_type_id.id,
                        'warehouse_id': picking.picking_type_id.warehouse_id.id,
                        'origin_returned_move_id': return_line.id,
                        'procure_method': 'make_to_stock',
                    }
                    r = return_line.copy(vals)
                    vals = {}
                    move_orig_to_link = return_line.move_dest_ids.mapped('returned_move_ids')
                    move_dest_to_link = return_line.move_orig_ids.mapped('returned_move_ids')
                    vals['move_orig_ids'] = [(4, m.id) for m in move_orig_to_link | return_line]
                    vals['move_dest_ids'] = [(4, m.id) for m in move_dest_to_link]
                    r.write(vals)

            new_picking.write({'rma_order_id': rma_order_create.id})
            if not returned_lines:
                raise UserError(_("Please specify at least one non-zero quantity."))

            new_picking.action_confirm()
            new_picking.action_assign()

        return request.render("website_rma.rma_thankyou")