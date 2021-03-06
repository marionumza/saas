# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_stock_dropshipping = fields.Boolean("Dropshipping")

    is_installed_sale = fields.Boolean(string="Is the Sale Module Installed")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            is_installed_sale=self.env['ir.module.module'].search([('name', '=', 'sale'), ('state', '=', 'installed')]).id,
        )
        return res
