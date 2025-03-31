#from odoo.tests.common import TransactionCase
#from odoo.exceptions import ValidationError
import logging
from odoo.tests import tagged

from .geral_functions import GeneralFunctions
@tagged('library')
class TestLibraryLoanLine(GeneralFunctions):

    logger = logging.getLogger(__name__)

    def setUp(self):
        self.logger.info('###LIBRARY LOAN LINE')
        super(TestLibraryLoanLine, self).setUp()
        self.author = self.env['library.author'].create({
            'name': 'Colleen Hoover',
            'birth': self.return_date('12/11/1979')
        })
        self.category = self.env['library.category'].create({
            'name': 'Romance'
        })
        self.book = self.env['library.book'].create({
            'title': 'It Ends with Us',
            'category': self.category,
            'author': self.author,
            'price_day': 7.5,
            'qty_stock': 10,
            'total_books': 10,
            'available': True
        })
        self.loan_lines = self.env['library.loan.lines'].create({
            'qty': 1,
            'due_date': self.return_date('03/16/2025'),
            'return_date': self.return_date('03/16/2025'),
            'loan_ids': self.loan.id,
            'book_ids': self.book.id
        })