# -*- coding: utf-8 -*-

import datetime
from harpiya.tests import common
from harpiya.fields import Datetime
from unittest.mock import patch


class EventSaleTest(common.TransactionCase):

    def setUp(self):
        super(EventSaleTest, self).setUp()

        self.EventRegistration = self.env['event.registration']

        # First I create an event product
        product = self.env['product.product'].create({
            'name': 'test_formation',
            'type': 'service',
            'event_ok': True,
        })

        # I create an event from the same type than my product
        event = self.env['event.event'].create({
            'name': 'test_event',
            'event_type_id': 1,
            'date_end': '2012-01-01 19:05:15',
            'date_begin': '2012-01-01 18:05:15'
        })

        ticket = self.env['event.event.ticket'].create({
            'name': 'test_ticket',
            'product_id': product.id,
            'event_id': event.id,
        })

        # I create a sales order
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_2').id,
            'note': 'Invoice after delivery',
            'payment_term_id': self.env.ref('account.account_payment_term_end_following_month').id
        })

        # In the sales order I add some sales order lines. i choose event product
        self.env['sale.order.line'].create({
            'product_id': product.id,
            'price_unit': 190.50,
            'product_uom': self.env.ref('uom.product_uom_unit').id,
            'product_uom_qty': 8.0,
            'order_id': self.sale_order.id,
            'name': 'sales order line',
            'event_id': event.id,
            'event_ticket_id': ticket.id,
        })

        # In the event registration I add some attendee detail lines. i choose event product
        self.register_person = self.env['registration.editor'].create({
            'sale_order_id': self.sale_order.id,
            'event_registration_ids': [(0, 0, {
                'event_id': event.id,
                'name': 'Administrator',
                'email': 'abc@example.com'
            })],
        })

    def test_00_create_event_product(self):
        # I click apply to create attendees
        self.register_person.action_make_registration()
        # I check if a registration is created
        registrations = self.EventRegistration.search([('origin', '=', self.sale_order.name)])
        self.assertTrue(registrations, "The registration is not created.")

    def test_event_is_registrable(self):
        self.patcher = patch('harpiya.addons.event.models.event.fields.Datetime', wraps=Datetime)
        self.mock_datetime = self.patcher.start()

        test_event = self.env['event.event'].create({
            'name': 'TestEvent',
            'date_begin': datetime.datetime(2019, 6, 8, 12, 0),
            'date_end': datetime.datetime(2019, 6, 12, 12, 0),
        })

        self.mock_datetime.now.return_value = datetime.datetime(2019, 6, 9, 12, 0)
        self.assertEqual(test_event._is_event_registrable(), True)

        self.mock_datetime.now.return_value = datetime.datetime(2019, 6, 13, 12, 0)
        self.assertEqual(test_event._is_event_registrable(), False)

        self.mock_datetime.now.return_value = datetime.datetime(2019, 6, 10, 12, 0)
        test_event.write({'event_ticket_ids': [(6, 0, [])]})
        self.assertEqual(test_event._is_event_registrable(), True)

        test_event_ticket = self.env['event.event.ticket'].create({
            'name': 'TestTicket',
            'event_id': test_event.id,
            'product_id': 1,
        })
        test_event_ticket.copy()
        test_event_ticket.product_id.active = False
        self.assertEqual(test_event._is_event_registrable(), False)

        self.patcher.stop()
