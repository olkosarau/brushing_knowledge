import logging
from odoo import api, fields, models


_logger = logging.getLogger(__name__)


class SplitManufacturingOrderWizard(models.TransientModel):
    _name = 'split.manufacturing.order.wizard'
    _description = 'Split Manufacturing Order Wizard'

    order_id = fields.Many2one('mrp.production', string="Order MRP")
    number_of_orders = fields.Integer(string='QTY order', required=True)
    order_mrp_line_ids = fields.One2many('split.manufacturing.order.line', 'order_mrp_id', string='Order Lines MRP')

    @api.model
    def _default_order_id(self):
        return self.env.context.get('default_order_id')

    # @api.onchange('number_of_orders')
    # def _onchange_number_of_orders(self):
    #     lines = []
    #     for i in range(self.number_of_orders):
    #         lines.append((0, 0, {'number_order': i + 1, 'qty_products': 0}))
    #     self.order_mrp_line_ids = lines

    @api.onchange('number_of_orders')
    def _onchange_number_of_orders(self):
        if self.number_of_orders > 0:
            product_qty = self.order_id.product_qty
            base_qty = product_qty // self.number_of_orders
            extra_qty = product_qty % self.number_of_orders

            lines = []
            current_lines = len(self.order_mrp_line_ids)
            for i in range(self.number_of_orders):
                qty = base_qty + 1 if i < extra_qty else base_qty
                if i < current_lines:
                    line = self.order_mrp_line_ids[i]
                    line.number_order = i + 1
                    line.qty_products = qty
                else:
                    lines.append((0, 0, {'number_order': i + 1, 'qty_products': qty}))

            self.order_mrp_line_ids = [(2, line.id) for line in self.order_mrp_line_ids[self.number_of_orders:]] + lines

    # @api.onchange('order_mrp_line_ids')
    # def _recalculate_order_lines(self):
    #     total_qty = sum(line.qty_products for line in self.order_mrp_line_ids)
    #     if len(self.order_mrp_line_ids) > 0:
    #         base_qty = total_qty // len(self.order_mrp_line_ids)
    #         extra_qty = total_qty % len(self.order_mrp_line_ids)
    #         for index, line in enumerate(self.order_mrp_line_ids):
    #             ln = self.order_mrp_line_ids[index]
    #             ln.number_order = index + 1
    #             ln.qty_products = base_qty + 1 if index < extra_qty else base_qty

    def continue_orders(self):
        active_id = self.env.context.get('default_order_id')
        original_order = self.env['mrp.production'].browse(active_id)
        new_orders = []

        for line in self.order_mrp_line_ids:
            new_order = original_order.copy()
            new_order.write({'origin': f'Split from {original_order.name}', 'product_qty': line.qty_products})
            new_orders.append(new_order.id)

        action = {
            'name': 'New Manufacturing Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', new_orders)],
        }
        return action


class SplitManufacturingOrderLine(models.TransientModel):
    _name = 'split.manufacturing.order.line'
    _description = 'Split Manufacturing Order Line'

    order_mrp_id = fields.Many2one('split.manufacturing.order.wizard', string="Order MRP", invisible=True)
    number_order = fields.Integer(string='Number Order')
    qty_products = fields.Integer(string='Quantity')

    @api.model
    def create(self, vals):
        order_mrp_id = vals.get('order_mrp_id')
        if order_mrp_id:
            order_lines = self.env['split.manufacturing.order.line'].search([('order_mrp_id', '=', order_mrp_id)])
            vals['number_order'] = len(order_lines) + 1
        return super(SplitManufacturingOrderLine, self).create(vals)
