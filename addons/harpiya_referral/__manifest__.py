# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.
{
    'name': "Harpiya referral program",
    'summary': """Allow you to refer your friends to Harpiya and get rewards""",
    'category': 'Hidden',
    'version': '1.0',
    'depends': ['base', 'web'],
    'data': [
        'views/templates.xml',
    ],
    'qweb': [
        "static/src/xml/systray.xml",
    ],
    'auto_install': True,
}
