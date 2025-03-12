from datetime import datetime
from .geral_functions import GeneralFunctions
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged('library')
class TestLibraryAuthor(GeneralFunctions):

    def setUp(self):
        super(TestLibraryAuthor, self).setUp()

        self.author = self.env['library.author'].create({
            'name': 'Clóvis de Barros Filho',
            'birth': self.convert_to_date('10/21/1966')
        })

    def test_create_author(self):
        name = 'Robert Martin'
        birth = self.convert_to_date('10/21/1952')
        new_author = self.env['library.author'].create({
            'name': name,
            'birth': birth
        })
        self.success_or_failed(new_author.name, name)

    def test_delete_author(self):
        new_author = self.env['library.author'].create({
            'name': 'Alex Ferguson',
            'birth': self.convert_to_date('10/21/1952')
        })
        id_author = new_author.id
        new_author.unlink()
        author_deleted = self.env['library.author'].browse(id_author)
        self.validation_param(not author_deleted.exists())

    def test_update_author(self):
        new_name = 'Clóvis de Barros'
        self.author.write({'name': new_name})
        self.success_or_failed(self.author.name, new_name)

