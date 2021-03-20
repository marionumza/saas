# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

{
    'name': 'HarpiyaBot',
    'version': '1.0',
    'category': 'Discuss',
    'summary': 'Add HarpiyaBot in discussions',
    'description': "",
    'website': 'https://www.harpiya.com/page/discuss',
    'depends': ['mail'],
    'installable': True,
    'application': False,
    'data': [
        'views/assets.xml',
        'views/res_users_views.xml',
        'data/mailbot_data.xml',
    ],
    'demo': [
        'data/mailbot_demo.xml',
    ],
    'qweb': [
        'views/discuss.xml',
    ],
}
