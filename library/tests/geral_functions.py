from datetime import datetime
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import tagged
import logging


class GeneralFunctions(TransactionCase):
    logger = logging.getLogger(__name__)
    name_test = ''

    def setUp(self):
        super(GeneralFunctions, self).setUp()
        self.logger.info(f"########/ {self.name_test} /########")

    def success_or_failed(self, param_1, param_2, name_test_param = ''):
        try:
            self.assertEqual(param_1, param_2)
            self.logger.info(f"{name_test_param}/TEST SUCCESS.")
        except AssertionError:
            self.logger.error(
                f"{name_test_param}/TEST FAILED.")
            raise

    def validation_param(self, IsTrue):
        if IsTrue:
            self.logger.info(f"AUTHOR, TEST SUCCESS.")
        else:
            self.logger.info(f"Param:{IsTrue} ")
            self.logger.error("AUTHOR, TEST FAILED")

    def convert_to_date(self, date_string):
        return datetime.strptime(date_string, '%m/%d/%Y').strftime('%Y-%m-%d')