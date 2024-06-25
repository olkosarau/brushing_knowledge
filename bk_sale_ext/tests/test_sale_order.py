from odoo.tests import TransactionCase
from odoo.exceptions import UserError

class TestSaleOrder(TransactionCase):

    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
            'sale_ok': True,
            'list_price': 100.0,
        })
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'sample_field': 'Initial Value',
        })
        self.sale_order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 1.0,
            'price_unit': self.product.list_price,
        })

    def test_action_trigger_user_error(self):
        self.sale_order.sample_field = 'Updated Value'
        with self.assertRaises(UserError):
            self.sale_order.action_trigger_user_error()

    def test_action_confirm(self):
        self.sale_order.action_confirm()
        pickings = self.sale_order.picking_ids
        self.assertEqual(len(pickings), 1)
        self.assertEqual(pickings.state, 'done')

    def test_action_confirm_with_express_delivery(self):
        self.sale_order_line.is_express_delivery = True
        self.sale_order.action_confirm()
        pickings = self.sale_order.picking_ids
        self.assertEqual(len(pickings), 1)
        self.assertIn('(Express)', pickings.origin)
        self.assertEqual(pickings.state, 'done')