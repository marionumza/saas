# -*- coding: utf-8 -*-
from harpiya import api, fields, models, _
from datetime import date


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date = fields.Date()
    recipients_of_email = fields.Many2many(comodel_name='res.partner', relation='customer', column1='partner_id',
                                           column2='partner_name', string="Recipients of the Email")
    subject = fields.Text('Subject')
    email_content = fields.Text('Email Content')

    @api.model
    def send_email_from_customer(self):
        today_date = date.today()
        current_date = str(today_date)
        obj = self.env['sale.order'].search([('state', 'in', ('sale', 'done'))])
        if obj:
            context = self._context
            current_uid = context.get('uid')
            current_login_user = self.env['res.users'].browse(current_uid)
            for order in obj:
                email_to = []
                order_date = str(order.date)
                if order and current_date == order_date:
                    for record in order.recipients_of_email:
                        if record.email:
                            email_to.append(record)

                    if email_to:
                        mail = {
                            'subject': order.subject,
                            'email_from': order.partner_id.email,
                            'recipient_ids': [(6, 0, [v.id for v in email_to])],
                            'body_html': order.email_content,
                        }

                        if mail:
                            mail_create = current_login_user.env['mail.mail'].create(mail)
                            if mail_create:
                                mail_create.send()
                                self.mail_id = mail_create
