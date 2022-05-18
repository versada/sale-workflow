# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    cancel_reason_id = fields.Many2one(
        comodel_name="sale.order.cancel.reason",
        string="Reason for cancellation",
        readonly=True,
        ondelete="restrict",
        tracking=True,
    )

    cancel_reason_description = fields.Text(
        string="Cancel reason",
        readonly=True,
    )

    def _show_cancel_wizard(self):
        res = super(SaleOrder, self)._show_cancel_wizard()
        if not self._context.get('by_pass_cancel_reason', False):
            for order in self:
                raison_count = self.env["sale.order.cancel.reason"].search_count(
                    order._get_sale_order_cancel_reason_domain())
                if raison_count > 0 and \
                    not order._context.get('disable_cancel_warning'):
                    return True
        return res

    def _get_sale_order_cancel_reason_domain(self):
        self.ensure_one()
        return [
            "|",
            ("company_id", "=", self.company_id.id),
            ("company_id", "=", False),
        ]


class SaleOrderCancelReason(models.Model):
    _name = "sale.order.cancel.reason"
    _description = "Sale Order Cancel Reason"

    name = fields.Char(string="Reason", required=True, translate=True)

    company_id = fields.Many2one(
        comodel_name="res.company",
    )

    need_description = fields.Boolean(
        string="Need Description",
    )
