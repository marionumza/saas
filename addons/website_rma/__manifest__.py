# -*- coding: utf-8 -*-
{
    "name": "Website RMA Return Orders Management Return Merchandise Authorization",
    "version": "13.0.0.2",
    "category": "eCommerce",
    "depends":
        [
            'base',
            'sale',
            'sale_management',
            'website',
            'website_sale','stock'
        ],
    "author": "BrowseInfo",
    'summary': 'Apps for website product Rma website return order eCommerce RMA shop Rma store Rma shop Return Merchandise Authorization return order from shop return item store return order Online RMA shop Request RMA website Request RMA return order request rma request',
    "description": "Website RMA Return Orders Management Return Merchandise Authorization",
    "website": "www.harpiya.com",
    "data": [
        'security/ir.model.access.csv',
        'views/rma_view.xml',
        'views/website_rma.xml',
        'views/rma_order_sequence.xml',
    ],
    "auto_install": False,
    "installable": True,
    "images": [
        'static/description/Banner.png'
    ],
}
