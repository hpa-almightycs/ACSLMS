from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


class Member(models.Model):
    # _name = 'acs.member'
    # _description = 'Member of the Library'
    _inherit = 'res.partner'

    is_member = fields.Boolean(string='Is Member')
    member_seq = fields.Char(string='Sequence', invisible=True)
    name = fields.Char(string='Name', required=True)

    # for multiple books one2many and many2one

    plan_name = fields.Many2one('product.product', string='Plan Name', store=True)
    book_plan_price = fields.Float(
        string='Book Plan Price', compute='_compute_book_plan_price', store=True
    )

    bstart_date = fields.Date(string='Plan Starting Date', default=date.today())
    bend_date = fields.Date(
        string='Plan Ending Date', compute='_compute_bend_date', store=True
    )

    pay_done = fields.Boolean(string='Pay  Due Button')
    show_pay_button = fields.Boolean(
        string='Show Pay Button', compute='_compute_show_pay_button', store=True
    )

### Visibility Of Button
    @api.depends('pay_done', 'bend_date')
    def _compute_show_pay_button(self):
        today = date.today()
        for record in self:
            if not record.pay_done:
                record.show_pay_button = True
            elif record.bend_date and record.bend_date > today:
                record.show_pay_button = False
            elif record.bend_date and record.bend_date <= today:
                record.show_pay_button = True
            else:
                record.show_pay_button = False
                
    

    # borrowed book button invoice
    def pay(self):
        self.ensure_one()
        if not self.plan_name:
            raise ValidationError('Plan is not selected')

        invoice_lines = [
            (
                0,
                0,
                {
                    'product_id': self.plan_name.id,
                    'price_unit': self.book_plan_price,
                },
            )
        ]

        pay = {
            'partner_id': self.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': invoice_lines,
        }

        invoice_obj = self.env['account.move'].create(pay)

        self.pay_done = True
        print(
            'payment done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        )
        self._compute_show_pay_button()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice_obj.id,
            'target': 'current',
        }

    ### Borrowing Books

    book_ids = fields.One2many('acs.bookline', 'member_id', string='Borrowed Books')
    book_id = fields.Many2one(
        'product.product',
        string='Books',
        default=lambda self: self.env['product.product'].search([], limit=1),
    )
    total_due = fields.Float(string='Total Due', store=False)

    due_done = fields.Boolean(string='Pay Button')
    show_due_button = fields.Boolean(string='Show Due Button', store=True)

    # , compute='_compute_show_due_button'

    ###plan duration
    @api.depends('bstart_date', 'plan_name')
    def _compute_bend_date(self):
        for record in self:
            if record.bstart_date and record.plan_name:
                bstart_date = fields.Date.from_string(record.bstart_date)
                if record.plan_name.name == '1 Month Borrow':
                    record.bend_date = bstart_date + relativedelta(months=+1)
                elif record.plan_name.name == '3 Months Borrow':
                    record.bend_date = bstart_date + relativedelta(months=+3)
                elif record.plan_name.name == '6 Months Borrow':
                    record.bend_date = bstart_date + relativedelta(months=+6)
                elif record.plan_name.name == '12 Months Borrow':
                    record.bend_date = bstart_date + relativedelta(months=+12)

    ### Calculating Total due
    @api.depends('book_ids.due_charge')
    def _compute_total_due(self):
        for record in self:
            record.total_due = sum(record.book_ids.mapped('due_charge'))

    ### Plan Price
    @api.depends('plan_name')
    def _compute_book_plan_price(self):
        for record in self:
            record.book_plan_price = (
                record.plan_name.list_price if record.plan_name else 0.0
            )

    # due charge invoice
    def due_charge(self):
        for record in self:
            if not record.book_ids:
                raise ValidationError('No books are selected for this member.')

        invoice_lines = []
        total_due_amount = 0

        for line in record.book_ids:
            if line.total_due > 0:
                invoice_lines.append(
                    (
                        0,
                        0,
                        {
                            'product_id': line.book_id.id,
                            'quantity': 1,
                            'price_unit': line.total_due,
                        },
                    )
                )
                total_due_amount += line.total_due

        if not invoice_lines:
            raise ValidationError('No overdue books to charge.')

        due_charge_vals = {
            'partner_id': self.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': invoice_lines,
        }

        invoice_obj = self.env['account.move'].create(due_charge_vals)

        for line in record.book_ids:
            if line.total_due > 0:
                line.total_due = 0
                line.last_payment_date = date.today()

        record.due_done = True

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice_obj.id,
            'target': 'current',
        }

      

    # membership duration

    joining_duration = fields.Many2one('product.product', string='Joining Duration')
    mfees = fields.Float(string='Product Price', compute='_compute_mfees', store=True)

    memb_start_date = fields.Date(string='Starting Date', default=date.today())
    memb_end_date = fields.Date(
        string='Ending Date', compute='_compute_memb_end_date', store=True
    )

    payment_done = fields.Boolean(string='Payment Button')
    renew_done = fields.Boolean(string='Renew Button')

    show_payment_button = fields.Boolean(
        string='Show Payment Button', compute='_compute_show_payment_button', store=True
    )
    show_renew_button = fields.Boolean(
        string='Show Renew Button', compute='_compute_show_payment_button', store=True
    )

    ### Visibality of button
    @api.depends('payment_done', 'memb_end_date')
    def _compute_show_payment_button(self):
        today = date.today()
        for record in self:
            if not record.payment_done:
                record.show_payment_button = True
                record.show_renew_button = False
            elif record.memb_end_date and record.memb_end_date <= today:
                record.show_payment_button = False
                record.show_renew_button = True
            else:
                record.show_payment_button = False
                record.show_renew_button = False

    ### Computing Price According to Plan
    @api.depends('joining_duration')
    def _compute_mfees(self):
        for record in self:
            if record.joining_duration:
                record.mfees = record.joining_duration.list_price

    ### Computing Date According to Plan
    @api.depends('memb_start_date', 'joining_duration')
    def _compute_memb_end_date(self):
        for record in self:
            if record.memb_start_date and record.joining_duration:
                start_date = fields.Date.from_string(record.memb_start_date)
                if record.joining_duration.name == '1 Month Member':
                    record.memb_end_date = start_date + relativedelta(months=+1)
                elif record.joining_duration.name == '3 Months Member':
                    record.memb_end_date = start_date + relativedelta(months=+3)
                elif record.joining_duration.name == '6 Months Member':
                    record.memb_end_date = start_date + relativedelta(months=+6)
                elif record.joining_duration.name == '12 Months Member':
                    record.memb_end_date = start_date + relativedelta(months=+12)

    ### Invoices
    def payment(self):
        self.ensure_one()

        if not self.joining_duration:
            raise ValidationError('Plan is not selected')

        invoice_lines = [
            (
                0,
                0,
                {
                    'product_id': self.joining_duration.id,
                    'price_unit': self.mfees,
                },
            )
        ]

        payment = {
            'partner_id': self.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': invoice_lines,
        }

        invoice_obj = self.env['account.move'].create(payment)

        self.payment_done = True

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice_obj.id,
            'target': 'current',
        }

    def renew(self):
        self.ensure_one()

        if not self.joining_duration:
            raise ValidationError('Plan is not selected')

        invoice_lines = [
            (
                0,
                0,
                {
                    'product_id': self.joining_duration.id,
                    'price_unit': self.mfees,
                },
            )
        ]

        renew = {
            'partner_id': self.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': invoice_lines,
        }

        invoice_obj = self.env['account.move'].create(renew)

        self.renew_done = False

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice_obj.id,
            'target': 'current',
        }

    ##### To prevent change of plan after payment  ###################################################################################

    def write(self, vals):
        if 'joining_duration' in vals:
            raise ValidationError('You can not change duration until it expires')
        if 'plan_name' in vals:
            raise ValidationError('You can not change plan until it expires')
        return super(Member, self).write(vals)

    ### Generating sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('member_seq', 'new') == 'new':
                vals['member_seq'] = self.env['ir.sequence'].next_by_code('acs.member')
        return super().create(vals_list)

    ### Unique Name

    def _check_unique(self):
        for record in self:
            existing_name = self.search([('name', '=', record.name)], limit=1)
            if existing_name and existing_name.id != record.id:
                raise ValidationError(
                    'The name is already taken by another member. Please choose a different name.'
                )

                    # f"The name '{record.name}' is already taken by another member. Please choose a different name."



    #### Either Author or Member
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
