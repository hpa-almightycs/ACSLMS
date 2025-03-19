from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class Author(models.Model):
    _inherit = 'res.partner'
    # _name = 'acs.author'


    is_author = fields.Boolean(string='Is Author')
    name = fields.Char(string='name')
   
    nationality = fields.Char(string='Nationality')
    category = fields.Selection(
        [
            ('comic', 'Comic'),
            ('philosophy','Philosophy'),
            ('divotee','Devotee'),
            ('biography','Biography'),
            ('mystery','Mystery'),
            ('poetry','Poetry'),
            ('novel','Novel'),
            ('thriller','Thriller'),
            ('fairy tale','Fairy Tale'),
            ('drama','Drama'),
            ('history','History'),
            ('other','Other'),
        ],
        string = 'Category',
        
    )  
   
   

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            existing_name = self.search([('name', '=', record.name)], limit=1)
            if existing_name and existing_name.id != record.id:
                raise ValidationError(
                    f"The name '{record.name}' is already taken by another author. Please choose a different name."
                )

###
    @api.onchange('is_author')
    def _onchange_is_author(self):
        if self.is_author:
            self.is_member = False

    @api.onchange('is_member')
    def _onchange_is_member(self):
        if self.is_member:
            self.is_author = False

    @api.constrains('is_author', 'is_member')
    def _check_exclusive_selection(self):
        for rec in self:
            if rec.is_author and rec.is_member:
                raise ValidationError('A person cannot be both an Author and a Member.')





