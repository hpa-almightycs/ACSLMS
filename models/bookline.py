from odoo import fields , models , api
from datetime import date
from dateutil.relativedelta import relativedelta


class LibraryBookLine(models.Model):
    _name = 'acs.bookline'
    _description = 'Library Book Line'

    member_id = fields.Many2one('res.partner', string='Member')
    book_id = fields.Many2one('product.product', string='Book')
    issue_date = fields.Date(string='Issue Date', default=date.today())
    return_date = fields.Date(string='Return Date', compute = '_compute_return_date', store = True)
    total_due = fields.Float(string='Due Charge', compute='_compute_due_charge', store = True)
    
    is_returned = fields.Boolean(string='Returned', default=False)
    last_payment_date = fields.Date(string='Last Payment Date')
    
    

    
    @api.depends('issue_date')
    def _compute_return_date(self):
        for record in self:
            record.return_date = record.issue_date + relativedelta(months=+1)
            
    ### Due charge
    @api.depends('return_date', 'is_returned', 'last_payment_date')
    def _compute_due_charge(self):
        for record in self:
            if record.is_returned:
                record.total_due = 0  
            else:
                if record.return_date and record.return_date < date.today():
                    if record.last_payment_date:
                        days_overdue = (date.today() - record.last_payment_date).days
                    else:
                        days_overdue = (date.today() - record.return_date).days
                
                    record.total_due = days_overdue * 1  
                else:
                    record.total_due = 0
  