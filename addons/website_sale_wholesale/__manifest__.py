# -*- coding: utf-8 -*-
{
    'name': "Website Sale Wholesale",
    'summary': "For wholesale customer for required login",
    'description': "For wholesale customer for required login",
    'author': "Harpiya Software Technologies",
    'website': "http://www.harpiya.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/harpiya/harpiya/blob/13.0/harpiya/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'eCommerce',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
