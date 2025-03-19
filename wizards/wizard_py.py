from odoo import models , api , fields

class Wizard(models.TransientModel):
    _name = 'acs.wizard'
    _description = 'ACS First Wizard'
    
    name = fields.Char(string = 'Name')
    staff_member = fields.Many2one('hr.employee',string='Staff Name')
    
    def sample_wizard(self):
        context = self.env.context
        print('Done, We added employee successfully')