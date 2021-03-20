# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya.addons.portal.controllers.portal import CustomerPortal
from harpiya.http import request


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        values['referral_updates_count'] = ''
        # Keep link to avoid having a pointless button
        values['referral_link'] = request.env.user._get_referral_link()
        return values
