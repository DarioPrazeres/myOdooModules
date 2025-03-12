from .geral_functions import GeneralFunctions

class TestLibraryLoan(GeneralFunctions):

    def setUp(self):
        self.name_test = 'LOAN'
        super(TestLibraryLoan, self).setUp()

        self.currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)

        self.user = self.env['res.partner'].create({
            'name': 'Johnny Deep',
            'email': 'johnnydeep@paratus.ao'
        })

        self.author = self.env['library.author'].create({
            'name': 'Colleen Hoover',
            'birth': self.convert_to_date('12/11/1979')
        })

        self.category = self.env['library.category'].create({
            'name': 'Romance'
        })

        self.book = self.env['library.book'].create({
            'title': 'It Ends with Us',
            'category': self.category.id,
            'author': self.author.id,
            'price_day': 7.5,
            'qty_stock': 10,
            'total_books': 10,
            'available': True
        })

        self.book1 = self.env['library.book'].create({
            'title': 'Verity',
            'category': self.category.id,
            'author': self.author.id,
            'price_day': 7.5,
            'qty_stock': 15,
            'total_books': 10,
            'available': True
        })

        self.loan = self.env['library.loan'].create({
            'user_id': self.user.id,
            'ref': 'LO0001',
            'loan_line_ids': [
                (0, 0, {
                    'qty': 1,
                    'due_date': self.convert_to_date('03/16/2025'),
                    'return_date': self.convert_to_date('03/16/2025'),
                    'book_ids': self.book.id,
                    'status': 'loan'
                }),
                (0, 0, {
                    'qty': 1,
                    'due_date': self.convert_to_date('03/20/2025'),
                    'return_date': self.convert_to_date('03/20/2025'),
                    'book_ids': self.book1.id,
                    'status': 'loan'
                }),
            ]
        })


    def test_create_loan_with_multiple_lines(self):
        self.logger.info("LOAN")
        self.success_or_failed(self.loan.user_id.id, self.user.id)
        self.logger.info(self.loan)

    def test_total_loan(self):
        #self.loan._compute_preco_total()
        price_total_calc_loan = sum(line.sub_total for line in self.loan.loan_line_ids)

        for line in self.loan.loan_line_ids:
            line._compute_day_loan()
        sub_total_formula = self.loan.loan_line_ids[0].day_loan * self.loan.loan_line_ids[0].price_book

        self.logger.info(f"{self.loan.loan_line_ids[0].sub_total}, {sub_total_formula}")

        self.success_or_failed(self.loan.price_total, price_total_calc_loan)

        self.success_or_failed(self.loan.loan_line_ids[0].sub_total, sub_total_formula)