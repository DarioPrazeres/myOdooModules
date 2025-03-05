from email.policy import default

from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import  ValidationError
from pkg_resources import require


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = "Library Loan"
    _inherit = ['mail.thread']

    book_id = fields.Many2one('library.book', string="Books")
    user_id = fields.Many2one('res.users')
    loan_date = fields.Date(string='Loan Date', default=fields.Date.today, required = True, tracking=True)
    return_date = fields.Date(string='Return date', tracking=True)
    due_date = fields.Date(string='Expected Return Date', required = True, tracking=True)
    status = fields.Selection([
        ('loan', 'Loan'),
        ('returned','Returned'),
        ('late','Late')
    ], default = 'loan', string="Status Loan", tracking=True)
    overdue_date = fields.Date(string="Overdue Date", tracking=True)

    def return_book(self):
        for rec in self:
            if rec.return_date and rec.return_date > rec.due_date:
                rec.status = 'overdue'
                rec.overdue_date = rec.return_date
            else:
                rec.status = 'returned'

            rec.book_id.available = True
            rec.book_id.write({'available': True})

    def create_loan(self):
        for rec in self:
            if rec.book_id.available:
                rec.boo_id.available = False
                rec.book_id.write({'available': False})

