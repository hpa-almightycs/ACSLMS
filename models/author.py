from odoo import models, fields, api

class Author(models.Model):
    _name = 'acs.author'
    _description = 'Author from ACS'

    author_id = fields.Integer(string='Author ID', required=True)
    name = fields.Char(string='Author', required=True)
    dob = fields.Date(string='Date of Birth', required=True)
    nationality = fields.Char(string='Nationality')
    category = fields.Char(string='Category')
    description = fields.Text(string='Description')
    # book = fields.Text(string='Books by Author')
    book_ids = fields.One2many('acs.book','author_id', string = 'Books by Author')
    
    
    
    
   
            