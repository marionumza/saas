# -*- coding: utf-8 -*-
{
    'name': "Notification Email From Sales Order",
    'author': 'Ascetic Business Solution',
    'category': 'Sales',
    'summary': """Notification Email From Sales Order""",
    'website': 'http://www.harpiya.com',
    'license': 'AGPL-3',
    'description': """ """,
    'version': '13.0.1.0',
    'depends': ['base','sale_management'],
    'data': ['views/sale_order_view.xml','views/scheduler_in_sale_order_view.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
