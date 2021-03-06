# -*- encoding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from . import controllers
from . import models
from . import wizard

import harpiya
from harpiya import api, SUPERUSER_ID
from functools import partial


def uninstall_hook(cr, registry):
    def rem_website_id_null(dbname):
        db_registry = harpiya.modules.registry.Registry.new(dbname)
        with api.Environment.manage(), db_registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            env['ir.model.fields'].search([
                ('name', '=', 'website_id'),
                ('model', '=', 'res.config.settings'),
            ]).unlink()
    cr.after('commit', partial(rem_website_id_null, cr.dbname))
