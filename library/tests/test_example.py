from odoo.tests.common import TransactionCase
import logging

class TestExample(TransactionCase):
    _logger = logging.getLogger(__name__)

    def setUp(self):
        super(TestExample, self).setUp()

        self.partner = self.env['res.partner'].create({'name': 'Test Partner'})

    def test_partner_name(self):
        self.assertEqual(self.partner.name, 'Test Partner')
        self._logger.info("Name is Equal, TEST SUCCESS")

    def test_change_partner_name(self):
        self.partner.name = 'New Name'
        self.assertEqual(self.partner.name, 'New Name')
