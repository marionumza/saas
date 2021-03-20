# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'New User Approval with webiste hide Price option',
    'description': 'New User Approval with webiste hide Price option',
    'summary': """ Facility to approve or reject new signed-up users.
    Get option to allow users sign-in only after email verification.
    It will not display your shop product price to the visitors until they log-in.""",
    'category': 'eCommerce',
    'version': '13.0.1.0.4',
    'author': 'Harpiya Software Technologies',
    'website': 'https://www.harpiya.com/',
    'depends': [
        'website_sale',
        'base_setup',
        'auth_signup',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/signup_mail.xml',
        'wizard/reject_msg_view.xml',
        'views/auth_signup_template.xml',
        'views/res_partner.xml',
        'views/signup_thank_template.xml',
        'views/website_user_view.xml',
        'views/res_config_view.xml',
    ],

    'images': [
        'static/description/banner.png'
    ],

    'installable': True,
    'application': False,
    'price': 18,
    'license': 'OPL-1',
    'currency': 'EUR',
}
