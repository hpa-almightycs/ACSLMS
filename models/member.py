from odoo import models, fields, api

class Member(models.Model):
    _name = 'acs.member'
    _description = 'Member of the Library'
    
    member_id = fields.Integer(string='Member ID', required=True)
    name = fields.Char(string='Name', required=True)
    dob = fields.Date(string='Date of Birth', required=True)
    emailid = fields.Char(string='Email ID', required=True)
    contactno = fields.Char(string='Contact No', required=True)
    subscription_fees = fields.Float(string='Subscription Fees')
    subscription_start_date = fields.Date(string='Subscription Starting Date')
    subscription_end_date = fields.Date(string='Subscription Ending Date')
    book_ids = fields.Many2many('acs.book','member_book_rel','member_id', 'book_id', string='Books')