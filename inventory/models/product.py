from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import  ValidationError

class InventoryProduct(models.Model):
    _name = 'inventory.product'
    _description = 'Product model for many thing'

    name = fields.Char(string='Name', required = True, tracking = True)
    price = fields.Float(string='Price', required = True, tracking = True)
    qty = fields.Integer(string='Quantity', required = True, tracking = True)
    category = fields.Many2one("inventory.category", string='Category', required = True, tracking = True)
