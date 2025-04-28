from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import  ValidationError

class InventoryStock(models.Model):
    _name = "inventory.stock"
    _description = "Stock of each product"

    product = fields.Many2one("inventory.product", string="Product", tracking = True, required = True)
    qty = fields.Integer(string="Quantity", tracking = True, required = True)
    date_move = fields.Date(string="Date Movement", tracking = True, required = True)
    move_type = fields.Selection([( 'input' , 'Input' ),( 'output' , 'Output' ),],
                                 string="Quantity", tracking = True, required = True)
    ref = fields.Char(string="Reference", default=lambda self: _('New'))
