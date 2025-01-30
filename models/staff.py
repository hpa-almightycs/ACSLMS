from odoo import models, fields, api

class Staff(models.Model):
    _name = 'acs.staff'
    _description = 'Staff'
    
    staff_id = fields.Integer(string='Staff ID', required=True)
    name = fields.Char(string='Name', required=True)
    emailid = fields.Char(string='Email ID', required=True)
    contactno = fields.Char(string='Contact No', required=True)
    dob = fields.Date(string='Date of Birth', required=True)
    # postion = fields.Char(string='Position', required=True)
    Position_Selection = [
        ('librerian','Librerian'),
        ('assistant_librerian','Assistant Librerian'),
        ('clerk','Clerk')
        ('cleaner','Cleaner')
        ('other','Other')
    ]
    
    position = fields.Selection(selection = Position_Selection,string = 'Position',required = True)
    