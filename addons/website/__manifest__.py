# -*- encoding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website',
    'category': 'Website/Website',
    'sequence': 7,
    'summary': 'Enterprise website builder',
    'website': 'https://www.harpiya.com/page/website-builder',
    'version': '1.0',
    'description': "",
    'depends': [
        'web',
        'web_editor',
        'http_routing',
        'portal',
        'social_media',
        'auth_signup',
    ],
    'installable': True,
    'data': [
        'data/website_data.xml',
        'data/website_visitor_cron.xml',
        'security/website_security.xml',
        'security/ir.model.access.csv',
        'views/website_templates.xml',
        'views/website_navbar_templates.xml',
        'views/snippets.xml',
        'views/website_views.xml',
        'views/website_visitor_views.xml',
        'views/res_config_settings_views.xml',
        'views/website_rewrite.xml',
        'views/ir_actions_views.xml',
        'views/ir_attachment_views.xml',
        'views/res_partner_views.xml',
        'wizard/base_language_install_views.xml',
    ],
    'demo': [
        'data/website_demo.xml',
    ],
    'qweb': ['static/src/xml/website.backend.xml'],
    'application': True,
    'uninstall_hook': 'uninstall_hook',
}