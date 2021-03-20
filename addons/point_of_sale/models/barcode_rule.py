# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import models, fields
from harpiya.tools.translate import _


class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    type = fields.Selection(selection_add=[
            ('weight', 'Weighted Product'),
            ('price', 'Priced Product'),
            ('discount', 'Discounted Product'),
            ('client', 'Client'),
            ('cashier', 'Cashier')
        ])
