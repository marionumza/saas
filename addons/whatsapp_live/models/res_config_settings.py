# -*- coding: utf-8 -*-

import logging
import urllib
import re

from harpiya import api, fields, models
from harpiya.exceptions import ValidationError


class Website(models.Model):
    _inherit = "website"

    whatsapp_number = fields.Char(string="Whatsapp Numarası")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    whatsapp_number = fields.Char(related='website_id.whatsapp_number', readonly=False,
                                  help="Ülke koduyla birlikte cep telefonu numarasını girin. (artı işareti ve özel "
                                       "karakter kullanmayın)")
