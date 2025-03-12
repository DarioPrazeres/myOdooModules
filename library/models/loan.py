from email.policy import default

from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError,  ValidationError
from pkg_resources import require
import logging




class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = "Library Loan"
    _inherit = ['mail.thread']
    _rec_name = 'ref'

    user_id = fields.Many2one('res.partner', 'Customer', required=True)
    name_partner = fields.Char(
        related='user_id.name',
        string="Name Customer")
    currency_id = fields.Many2one('res.currency', string="Currency", required=True,
                                  default=lambda self: self.env.company.currency_id)
    loan_line_ids = fields.One2many('library.loan.line', 'loan_ids', string="Loan Line")
    price_total = fields.Float(compute='_compute_preco_total', store=True, string="Total")
    #price_total = fields.Float(store=True, string="Total", currency_field='currency_id')
    ref = fields.Char(string="Reference", default=lambda self: _('New'))

    def return_book(self):
        for rec in self:
            for loan_line in rec.loan_line_ids:
                date_return = loan_line.return_date

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

    @api.onchange("return_date")
    def compute_return_date(self):
        for rec in self:
            if rec.return_date and rec.return_date > rec.due_date:
                rec.status = 'overdue'
                rec.overdue_date = rec.return_date
                rec.book_id.available = True
                rec.book_id.write({'available':True})
            elif rec.return_date <= rec.due_date:
                rec.status = 'returned'
                rec.book_id.available = True
                rec.book_id.write({'available':True})
            else:
                rec.status = 'loan'
                rec.book_id.available = False
                rec.book_id.write({'available':False})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
           vals['ref'] = self.env['ir.sequence'].next_by_code('library.loan')
        return super(LibraryLoan, self).create(vals_list)

    #@api.depends('loan_line_ids.sub_total')
    @api.onchange('loan_line_ids.sub_total')
    def _compute_preco_total(self):
        for loan in self:
            loan.price_total = sum(line.sub_total for line in loan.loan_line_ids)


class LibraryLoanLine(models.Model):
    _name = 'library.loan.line'
    _description = "Library Loan Line"
    _inherit = ['mail.thread']

    _logger = logging.getLogger(__name__)

    loan_ids = fields.Many2one('library.loan', string="Loan")
    book_ids = fields.Many2one('library.book',
                               string="Books",
                               domain="[('available', '=', True), ('qty_stock','>','0')]",
                               required=True)
    price_book = fields.Float(
        related='book_ids.price_day',
        string="Per Day (KZ)",
        store=True)
    qty = fields.Integer(string="Quantity", default = 0,tracking=True)
    loan_date = fields.Date(string='Loan day', default=fields.Date.today, required = True, tracking=True)
    return_date = fields.Date(string='Return day', store=True, tracking=True)
    due_date = fields.Date(string='Due Date', required = True, tracking=True)
    status = fields.Selection([
        ('loan', 'Loan'),
        ('returned','Returned'),
        ('overdue','Overdue')
    ], default = 'loan', string="Status Loan", tracking=True)
    overdue_date = fields.Date(string="Overdue Date", tracking=True)

    day_loan = fields.Integer(string="Day Loan", store=True, compute='_compute_day_loan', default=0)
    sub_total = fields.Float(string="Subtotal", store=True, default=0, tracking=True)
    total = fields.Integer(string="Total", compute='_compute_total', store=True, default=0)

    @api.depends('loan_date', 'due_date')
    def _compute_day_loan(self):
        for rec in self:
            if rec.due_date:
                rec.day_loan = rec.due_date.day - rec.loan_date.day
                if rec.day_loan <= 0:
                    UserError(_('Date Due is incorrect!'))
                    rec.due_date = fields.Date.today()
                    rec.day_loan = 0
                else:
                    rec.sub_total = rec.day_loan * rec.price_book

    @api.onchange('qty')
    def onchange_qty(self):
        if self.qty:
            if self.qty > 0 and self.book_ids.qty_stock < self.qty:
                self.qty = self.book_ids.qty_stock

    @api.onchange('return_date')
    def onchange_return_date(self):
        if self.return_date:
            if self.return_date > self.due_date:
                self.qty = self.book_ids.qty_stock

    @api.constrains('due_date')
    def _check_due_date(self):
        for rec in self:
            if rec.due_date < fields.Date.today():
                raise UserError("The due date cannot be set in the past")

    @api.model_create_multi
    def create(self, vals_list):
        available_qty = 0
        today = fields.Date.today()
        for vals in vals_list:
            qty_selected = vals.get('qty', 1)
            book = self.env['library.book'].browse(vals['book_ids'])

            #total_loans = sum(self.search([('book_ids', '=', book.id)]).mapped('qty'))
            self._logger.info(f"Processing book: {book.id}, vals: {vals},"
                              f"Valores gerais:{vals_list}")

            return_date = vals.get('return_date')
            due_date = vals.get('due_date', today)

            if return_date and due_date:
                # Are dates in Right format(Date) for comparation
                if isinstance(return_date, str):
                    return_date = fields.Date.from_string(return_date)
                if isinstance(due_date, str):
                    due_date = fields.Date.from_string(due_date)

                # Camparar Dates
                if return_date < due_date:
                    available_qty = book.qty_stock + qty_selected
                    if available_qty > 0:
                        raise ValidationError(f"Books Available: {book.qty_stock}")

            else:
                available_qty = book.qty_stock - qty_selected
                if available_qty < 0:
                    raise ValidationError(f"There is no books available enough. ,"
                                          f"Books Available: {book.qty_stock}")

            book.qty_stock = available_qty
            book.write({'qty_stock': book.qty_stock})
            if book.qty_stock <= 0: book.write({'available': False})

        return super().create(vals_list)

    def write(self, values):
        #self.book_ids.qty_stock = self.book_ids.total_books - self.qty
        #self.book_ids.write({'qty_stock': self.book_ids.qty_stock})
        return super().write(values)


