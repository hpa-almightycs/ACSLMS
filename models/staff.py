from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class Staff(models.Model):
    _inherit = 'hr.employee'
    
    staff_seq = fields.Char(string='Sequence', invisible=True)
   


    
    position = fields.Selection(
        [
            ('librerian', 'Librerian'),
            ('assistant_librerian', 'Assistant Librerian'),
            ('clerk', 'Clerk'),
            ('cleaner', 'Cleaner'),
            ('other', 'Other'),
        ],
        string='Select Position'
    )


### Wizardddd
    def open_wizard(self):
        return{
            'name':'Select Employee',
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'res_model':'acs.wizard',
            'target':'new',
            'context':{'custom_employee_id':self.id}
        }
    

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = ''  
            if vals.get('staff_seq', 'new') == 'new':
                vals['staff_seq'] = self.env['ir.sequence'].next_by_code('acs.staff')
        return super().create(vals_list)
    

       
       

    # dob = fields.Date(string='Date of Birth', required=True)
    # age = fields.Integer(string='Age', compute='compute_age', store=True)    
    
    
    # @api.depends('dob')
    # def compute_age(self):
    #     for staff in self:
    #         if staff.dob:
    #             today = date.today()
    #             age = today.year - staff.dob.year - ((today.month, today.day) < (staff.dob.month, staff.dob.day))
    #             staff.age = age
    #         else:
    #             staff.age = 0

    # @api.onchange('dob')
    # def _check_staff_age(self):
    #     if self.dob:
    #         today = date.today()
    #         age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    #         if age < 18:
    #             return {
    #                 'warning': {
    #                     'title': 'Age Warning',
    #                     'message': 'The staff member is under 18 years of age. Please ensure this is correct.',
    #                 }
    #             }

  
            
            
            
