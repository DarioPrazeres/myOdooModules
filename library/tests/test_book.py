from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import tagged
import logging

@tagged('library')
class TestLibraryBook(TransactionCase):
    title = 'The Subtle Art of Not Giving a F*ck'
    available = True
    price_day = 5.75
    qty_stock = 10
    _logger = logging.getLogger(__name__)

    def setUp(self):
        super(TestLibraryBook, self).setUp()

        self.author = self.env['library.author'].create({
            'name': 'Mark Mason'
        })
        self.category = self.env['library.category'].create({
            'name': 'Self-Improvement'
        })
        self.book = self.env['library.book'].create({
            'title': self.title,
            'author': self.author.id,
            'category': self.category.id,
            'available': self.available,
            'price_day': self.price_day,
            'qty_stock': self.qty_stock
        })

    def test_create_book(self):
        t = 'Everything Is F*cked!'
        book = self.env['library.book'].create({
            'title': t,
            'author': self.author.id,
            'category': self.category.id,
            'available': self.available,
            'price_day': self.price_day,
            'qty_stock': self.qty_stock
        })

        self.success_or_failed(book.title, t)
        self.success_or_failed(book.capitalizeTitle, t.upper())
        self.validation_param(book.ref.startswith('BK'))

    def test_onchange_qty_stock(self):
        self.qty_stock = 0

        self.book.qty_stock = 5
        self.book.onchange_qty_stock()
        self.validation_param(self.book.available)

    def test_read_book(self):
        book = self.env['library.book'].search([('name', '=', 'The Subtle Art of Not Giving a F*ck')])

        self.success_or_failed(book.name, 'The Subtle Art of Not Giving a F*ck')
        self.success_or_failed(book.author.name, 'Mark Mason')

    def test_delete_book(self):
        book_to_delete = self.env['library.book'].create({
            'title': 'The Hate you Love',
            'author': self.author.id,
            'category': self.category.id,
            'available': True,
            'price_day': 7.5,
            'qty_stock': 1
        })
        book_to_delete_id = book_to_delete.id
        book_to_delete.unlink()
        book_after_delete = self.env['library.book'].browse(book_to_delete_id)
        self.validation_param(not book_after_delete.exists())

    def success_or_failed(self, param_1, param_2):
        try:
            self.assertEqual(param_1, param_2)
            self._logger.info("BOOK, TEST SUCCESS.")
        except AssertionError:
            self._logger.error(
                f"BOOK, TEST FAILED.")
            raise

    def validation_param(self, IsTrue):
        if IsTrue:
            self._logger.info(f"BOOK, TEST SUCCESS.")
        else:
            self._logger.info(f"Param:{IsTrue} ")
            self._logger.error("BOOK, TEST FAILED")
