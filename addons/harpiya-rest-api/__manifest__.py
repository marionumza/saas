# -*- coding: utf-8 -*-
{
    'name': "Harpiya REST API",

    'summary': """
        Harpiya REST API""",

    'description': """
        Harpiya REST API
    """,

    'author': "Harpiya Software Technologies",
    'website': "https://harpiya.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/harpiya/harpiya/blob/12.0/harpiya/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Developers',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    "application": True,
    "installable": True,
    "auto_install": True,

    'external_dependencies': {
        'python': ['pypeg2', 'requests']
    }
}