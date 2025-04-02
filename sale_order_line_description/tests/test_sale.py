# Copyright 2017 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSaleOrderLineDescriptionChange(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create models
        cls.sale_order_model = cls.env["sale.order"]
        cls.sale_order_line_model = cls.env["sale.order.line"]
        cls.partner_model = cls.env["res.partner"]
        cls.product_model = cls.env["product.product"]
        cls.user_model = cls.env["res.users"].with_context(
            no_reset_password=True, mail_create_nosubscribe=True
        )

        # Create user group
        cls.group_only_sale_description = cls.env.ref(
            "sale_order_line_description.group_use_product_description_per_so_line"
        )

        # Create the sale order
        cls.partner = cls.partner_model.create({"name": "Test partner"})
        cls.sale_order = cls.sale_order_model.create({"partner_id": cls.partner.id})

        cls.product = cls.product_model.create(
            {
                "name": "Test product",
                "description_sale": "Sale description for test product",
            }
        )
        cls.line_values = {"order_id": cls.sale_order.id, "product_id": cls.product.id}

    def _create_user(self, name, group=None):
        groups_id = self.env.user.groups_id
        if group:
            groups_id += group
        return self.user_model.create(
            {
                "name": name,
                "login": name,
                "email": name + "@example.com",
                "groups_id": groups_id,
            }
        )

    def test_01_check_sale_order_line_description_standard(self):
        # GIVEN
        self.user_1 = self._create_user("TestUser1")
        # WHEN
        sale_order_line = self.sale_order_line_model.with_user(self.user_1).create(
            self.line_values.copy()
        )
        # THEN
        self.assertEqual(
            sale_order_line.name,
            "\n".join([self.product.name, self.product.description_sale]),
            "Standard behavior does not concatenate "
            "product description and product sale description",
        )

    def test_02_check_sale_order_line_description_with_group(self):
        # GIVEN
        self.user_2 = self._create_user("TestUser2", self.group_only_sale_description)
        # WHEN
        sale_order_line = self.sale_order_line_model.with_user(self.user_2).create(
            self.line_values.copy()
        )
        # THEN
        self.assertEqual(
            sale_order_line.name,
            self.product.description_sale,
            "Adding group "
            + self.group_only_sale_description.name
            + " does not modify sale order line description",
        )
