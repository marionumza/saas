# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import models, _

class LinkTracker(models.Model):
    _inherit = ['link.tracker']

    def action_visit_page_statistics(self):
        return {
            'name': _("Visit Webpage Statistics"),
            'type': 'ir.actions.act_url',
            'url': '%s+' % (self.short_url),
            'target': 'new',
        }
