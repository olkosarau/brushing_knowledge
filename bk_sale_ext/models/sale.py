from odoo import models, fields, api
from odoo.exceptions import ValidationError



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):

        normal_lines = self.order_line.filtered(lambda line: not line.is_express_delivery)
        express_lines = self.order_line.filtered(lambda line: line.is_express_delivery)

        if normal_lines:
            picking = self._create_delivery_picking(normal_lines)
            self.write({'picking_ids': [(4, picking.id)]})
            picking.with_context(skip_immediate=True).button_validate()
            picking.write({'state': 'done'})

        if express_lines:
            express_picking = self._create_delivery_picking(express_lines, express=True)
            self.write({'picking_ids': [(4, express_picking.id)]})
            express_picking.with_context(skip_immediate=True).button_validate()
            express_picking.write({'state': 'done'})

        return True

    def _create_delivery_picking(self, order_lines, express=False):
        picking_type = self.env.ref('stock.picking_type_out')
        picking_vals = {
            'picking_type_id': picking_type.id,
            'partner_id': self.partner_id.id,
            'origin': self.name,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': self.partner_id.property_stock_customer.id,
            'move_ids': [(0, 0, {
                'name': line.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': self.partner_id.property_stock_customer.id,
                'sale_line_id': line.id,
            }) for line in order_lines]
        }

        if express:
            picking_vals['origin'] += ' (Express)'

        return self.env['stock.picking'].create(picking_vals)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_id_domain_ids = fields.Many2many('product.product', compute='_compute_product_id_domain')
    is_express_delivery = fields.Boolean(string="Express Delivery")

    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        change_default=True,
        ondelete='restrict',
        index=True,
        domain=[('sale_ok', '=', True), ('id', 'in', product_id_domain_ids)]
    )

    @api.depends('order_id', 'order_id.order_line.product_id')
    def _compute_product_id_domain(self):
        for line in self:
            if line.order_id:
                selected_product_ids = line.order_id.order_line.mapped('product_id.id')
                line.product_id_domain_ids = self.env['product.product'].search([('sale_ok', '=', True), ('id', 'not in', selected_product_ids)]).ids
            else:
                line.product_id_domain_ids = self.env['product.product'].search([('sale_ok', '=', True)]).ids
