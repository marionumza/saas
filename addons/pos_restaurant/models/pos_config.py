# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    iface_splitbill = fields.Boolean(string='Bill Splitting', help='Enables Bill Splitting in the Point of Sale.')
    iface_printbill = fields.Boolean(string='Bill Printing', help='Allows to print the Bill before payment.')
    iface_orderline_notes = fields.Boolean(string='Orderline Notes', help='Allow custom notes on Orderlines.')
    floor_ids = fields.One2many('restaurant.floor', 'pos_config_id', string='Restaurant Floors', help='The restaurant floors served by this point of sale.')
    printer_ids = fields.Many2many('restaurant.printer', 'pos_config_printer_rel', 'config_id', 'printer_id', string='Order Printers')
    is_table_management = fields.Boolean('Table Management')
    is_order_printer = fields.Boolean('Order Printer')
    module_pos_restaurant = fields.Boolean(default=True)

    @api.onchange('module_pos_restaurant')
    def _onchange_module_pos_restaurant(self):
        if not self.module_pos_restaurant:
            self.update({'iface_printbill': False,
            'iface_splitbill': False,
            'is_order_printer': False,
            'is_table_management': False,
            'iface_orderline_notes': False})

    @api.onchange('is_table_management')
    def _onchange_is_table_management(self):
        if not self.is_table_management:
            self.floor_ids = [(5, 0, 0)]

    @api.onchange('is_order_printer')
    def _onchange_is_order_printer(self):
        if not self.is_order_printer:
            self.printer_ids = [(5, 0, 0)]

    def get_tables_order_count(self):
        """         """
        self.ensure_one()
        tables = self.env['restaurant.table'].search([('floor_id.pos_config_id', 'in', self.ids)])
        domain = [('state', '=', 'draft'), ('table_id', 'in', tables.ids)]

        order_stats = self.env['pos.order'].read_group(domain, ['table_id'], 'table_id')
        orders_map = dict((s['table_id'][0], s['table_id_count']) for s in order_stats)

        result = []
        for table in tables:
            result.append({'id': table.id, 'orders': orders_map.get(table.id, 0)})
        return result
