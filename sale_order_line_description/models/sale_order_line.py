# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_sale_order_line_multiline_description_sale(self):
        if (
            self.env.user.has_group(
                "sale_order_line_description."
                "group_use_product_description_per_so_line"
            )
            and self.product_id.description_sale
        ):
            product = self.product_id
            if self.order_id.partner_id:
                product = product.with_context(
                    lang=self.order_id.partner_id.lang,
                )
            return product.description_sale
        return super()._get_sale_order_line_multiline_description_sale()
