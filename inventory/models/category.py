from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import  ValidationError

class LibraryCategory(models.Model):
    _name = "inventory.category"
    _description = "Product Category"

    name = fields.Char(string = "Name", required = True, tracking = True)