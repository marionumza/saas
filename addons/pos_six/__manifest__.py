# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.
{
    'name': 'POS Six',
    'version': '1.0',
    'category': 'Sales/Point Of Sale',
    'sequence': 6,
    'summary': 'Integrate your POS with a Six payment terminal',
    'description': '',
    'data': [
        'views/pos_payment_method_views.xml',
        'views/point_of_sale_assets.xml',
    ],
    'depends': ['point_of_sale'],
    'installable': True,
    'license': 'OEEL-1',
}
