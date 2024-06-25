from odoo.tests import TransactionCase

class TestMrpProduction(TransactionCase):

    def setUp(self):
        super(TestMrpProduction, self).setUp()
        self.production_order = self.env['mrp.production'].create({
            'product_id': self.env.ref('product.product_product_1').id,
            'product_qty': 1.0,
            'product_uom_id': self.env.ref('uom.product_uom_unit').id,
            'bom_id': self.env.ref('mrp.mrp_bom_1').id,
            'location_src_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
        })

    def test_run_split_production_order(self):
        action = self.production_order.run_split_production_order()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'split.manufacturing.order.wizard')
        self.assertEqual(action['view_mode'], 'form')
        self.assertEqual(action['target'], 'new')
        self.assertIn('default_order_id', action['context'])
        self.assertEqual(action['context']['default_order_id'], self.production_order.id)