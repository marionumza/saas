# Part of Harpiya. See LICENSE file for full copyright and licensing details.

from harpiya import fields, models


class Survey(models.Model):
    _inherit = 'survey.survey'

    category = fields.Selection(selection_add=[('hr_recruitment', 'Recruitment')])
