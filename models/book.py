from odoo import models, fields, api

class Book(models.Model):
    _name = 'acs.book'
    _description = 'Book by ACS'
    
    
    name = fields.Char(string='Book Name', required=True)
    language = fields.Char(string='Language of Book', required=True)
    description = fields.Text(string='Description')
    publisher = fields.Char(string='Publisher')
    category = fields.Char(string='Category')
    author_id = fields.Many2one('acs.author', string = 'Author', required=True)
    