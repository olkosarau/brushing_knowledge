from odoo import _, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # def run_split_production_order(self):
    #     return self.env['ir.actions.act_window']._for_xml_id('bk_mrp_ext.action_split_manufacturing_order_wizard')

    def run_split_production_order(self):
        self.ensure_one()
        view_id = self.env.ref('bk_mrp_ext.view_split_manufacturing_order_wizard').id
        return {
            'name': _('Split Manufacturing Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'split.manufacturing.order.wizard',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'context': {
                'default_order_id': self.id,
            },
        }