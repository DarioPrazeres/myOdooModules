
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import  ValidationError


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library"
    _inherit = ['mail.thread']

    name = fields.Char(string="Name", store=True)
    title = fields.Char(string = "Title", required = True, tracking = True)
    author = fields.Many2one("library.author", string = "Author", required = True, tracking = True)
    category = fields.Many2one("library.category", string = "Category", required = True, tracking = True)
    available = fields.Boolean(string = "Available", required = True, tracking = True)
    datePost = fields.Date(string = "Post", tracking = True)
    cover = fields.Binary(string = "Cover", tracking=True)
    description = fields.Text(string="Description", tracking=True)
    price_day = fields.Float(string="Price per Day", required=True, tracking=True)
    capitalizeTitle = fields.Char(compute= "_compute_upper")

    qty_stock = fields.Integer(string="Qty Available", required=True, tracking=True)
    total_books = fields.Integer(string="Total Book", store=True)
    ref = fields.Char(string="Reference", default=lambda self: _('New'))

    @api.onchange('qty_stock', 'available')
    def onchange_qty_stock(self):
        if self.qty_stock:
            if self.qty_stock > 0:
                self.available = True


    @api.depends("title")
    def _compute_upper(self):
        for rec in self:
            rec.name = rec.title if rec.title else ''
            rec.capitalizeTitle = rec.title.upper() if rec.title else ''

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
           vals['ref'] = self.env['ir.sequence'].next_by_code('library.book')
        return super(LibraryBook, self).create(vals_list)