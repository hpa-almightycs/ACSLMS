from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import datetime

class BookStoreLine(models.Model):
    _name = 'acs.bookstoreline'
    _description = 'To order multiple books'
    
    book_product = fields.Many2one('product.product', string='Books')
    price_line = fields.Float(string='Price', compute='_compute_price')
    quantity_line = fields.Integer(string='No. of Books')
    total_price_line = fields.Float(string='Total Price', compute='_compute_total_price_line')
    order_id = fields.Many2one('acs.bookstore', string='Book Order') 


    ### Listing Book Price
    @api.depends('book_product')
    def _compute_price(self):
        for record in self:
            record.price_line = record.book_product.list_price
    
    ### Computin Book Price According to Quantity
    @api.depends('price_line', 'quantity_line')
    def _compute_total_price_line(self):
        for record in self:
            record.total_price_line = record.price_line * record.quantity_line
            
            
    
   
    
    
  