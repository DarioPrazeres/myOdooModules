from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import  ValidationError

class LibraryAuthor(models.Model):
    _name = "library.author"
    _description = "Book Author"

    name = fields.Char(string="Name", required = True, tracking = True)
    birth = fields.Date(string="Birth", tracking = True)
