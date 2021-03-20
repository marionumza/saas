# -*- coding: utf-8 -*-

# from harpiya import models, fields, api


# class website_sale_wholesale(models.Model):
#     _name = 'website_sale_wholesale.website_sale_wholesale'
#     _description = 'website_sale_wholesale.website_sale_wholesale'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
