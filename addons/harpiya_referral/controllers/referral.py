# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya.http import Controller, request, route


class Referral(Controller):

    @route(['/harpiya_referral/go'], type='json', auth='user', method='POST', website=True)
    def referral_go(self):
        return {'link': request.env.user._get_referral_link(reset_count=True)}
