# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from harpiya import api, fields, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    discount_total = fields.Monetary(
        compute="_compute_amount", string="Discount Subtotal", store=True
    )
    price_total_no_discount = fields.Monetary(
        compute="_compute_amount", string="Subtotal Without Discount", store=True
    )

    def _update_discount_display_fields(self):
        if self.env.context.get('website_id'):
            current_website = self.env['website'].get_current_website()
            if current_website.wholesale and current_website.product_series:
                for line in self:
                    line.price_total_no_discount = 0
                    line.discount_total = 0
                    series = line.product_id.wholesale_series
                    if not line.discount:
                        line.price_total_no_discount = line.price_total
                        continue
                    price = line.price_unit
                    taxes = line.tax_id.compute_all(
                        price,
                        line.order_id.currency_id,
                        line.product_uom_qty,
                        product=line.product_id,
                        partner=line.order_id.partner_shipping_id,
                    )

                    price_total_no_discount = taxes["total_included"]
                    discount_total = -((price_total_no_discount * series) - line.price_total)
                    print("İndirim {}".format(line.price_total))

                    line.update(
                        {
                            "discount_total": discount_total,
                            "price_total_no_discount": price_total_no_discount * series,
                        }
                    )
        else:
            for line in self:
                line.price_total_no_discount = 0
                line.discount_total = 0
                if not line.discount:
                    line.price_total_no_discount = line.price_total
                    continue
                price = line.price_unit
                taxes = line.tax_id.compute_all(
                    price,
                    line.order_id.currency_id,
                    line.product_uom_qty,
                    product=line.product_id,
                    partner=line.order_id.partner_shipping_id,
                )

                price_total_no_discount = taxes["total_included"]
                discount_total = -(price_total_no_discount - line.price_total)

                line.update(
                    {
                        "discount_total": discount_total,
                        "price_total_no_discount": price_total_no_discount,
                    }
                )

    @api.depends("product_uom_qty", "discount", "price_unit", "tax_id")
    def _compute_amount(self):
        res = super(SaleOrderLine, self)._compute_amount()
        self._update_discount_display_fields()
        return res
