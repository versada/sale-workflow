# © 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderCancel(models.TransientModel):

    """Ask a reason for the sale order cancellation."""

    _inherit = "sale.order.cancel"

    reason_id = fields.Many2one(
        comodel_name="sale.order.cancel.reason",
        required=True,
    )

    allowed_reason_ids = fields.Many2many(
        comodel_name="sale.order.cancel.reason",
        compute="_compute_display_cancel_reason",
    )

    display_cancel_reason = fields.Boolean(
        string="Display Cancel Reason",
        compute="_compute_display_cancel_reason",
    )

    @api.depends('order_id')
    def _compute_display_cancel_reason(self):
        for wizard in self:
            raisons = self.env["sale.order.cancel.reason"].search(
                wizard.order_id._get_sale_order_cancel_reason_domain())
            wizard.allowed_reason_ids = raisons
            wizard.display_cancel_reason = bool(len(raisons))

    def action_cancel(self):
        self.ensure_one()
        res = super().action_cancel()
        self.order_id.cancel_reason_id = self.reason_id
        return res
