# -*- coding: utf-8 -*-
# Part of Harpiya. See LICENSE file for full copyright and licensing details.
from harpiya.tests.common import TransactionCase
from dateutil.relativedelta import relativedelta


class TestContractBase(TransactionCase):

    def setUp(self):
        super(TestContractBase, self).setUp()

        self.employee = self.env['hr.employee'].create({
            'name': 'Richard',
            'gender': 'male',
            'country_id': self.ref('base.be'),
        })
