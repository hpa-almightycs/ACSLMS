from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class Bookstore(models.Model):
    _name = 'acs.bookstore'
    _description = 'Book Store of ACS Library'

    bookstore_seq = fields.Char(string='Sequence', invisible=True)
    customer_name = fields.Many2one(
        'res.partner', string='Customer Name', required=True
    )
    book_product = fields.Many2one(
        'product.product',
        string='Book',
        default=lambda self: self.env['product.product'].search([], limit=1),
    )
    book_order_lines = fields.One2many('acs.bookstoreline', 'order_id', string='Books')
    today_date = fields.Date(
        string='Date', default=fields.Date.context_today, readonly=True
    )
    total_price = fields.Float(
        string='Total Price', compute='_compute_total_price', store=True
    )

    paid = fields.Boolean(string='Paid')
    show_pay_button = fields.Boolean(
        string='Show Pay Button', compute='_compute_show_pay_button', store=True
    )


########## Smart Button ############################
    total_payment = fields.Float(
        string='Total Payment', compute='_compute_total_amount', store=True
    )

    @api.depends('customer_name')
    def _compute_total_amount(self):
        for record in self:
            if record.customer_name:
                invoices = self.env['account.move'].search(
                    [
                        ('partner_id', '=', record.customer_name.id),
                        ('move_type', '=', 'out_invoice'),
                        ('amount_total', '>', 0),
                    ]
                )

                total_paid = sum(
                    invoice.amount_total
                     for invoice in invoices
                    if invoice.amount_residual == 0
                )
                record.total_payment = total_paid
            else:
                record.total_payment = 0.0



    def action_view_total_payment(self):
        self.ensure_one()  
        invoices = self.env['account.move'].search(
        [
            ('partner_id', '=', self.customer_name.id),
            ('move_type', '=', 'out_invoice'),
        ]
    )
        return {
        'type': 'ir.actions.act_window',
        'name': 'Invoices',
        'res_model': 'account.move',
        'view_mode': 'list,form',
        'domain': [('id', 'in', invoices.ids)],
        'target': 'current',
    }

    ### Visibility of Button
    @api.depends('paid')
    def _compute_show_pay_button(self):
        for record in self:
            if not record.paid:
                record.show_pay_button = True
            else:
                record.show_pay_button = False

    ### Allover price
    @api.depends('book_order_lines.total_price_line')
    def _compute_total_price(self):
        for record in self:
            record.total_price = sum(
                line.total_price_line for line in record.book_order_lines
            )

    ### Sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('bookstore_seq', 'new') == 'new':
                vals['bookstore_seq'] = self.env['ir.sequence'].next_by_code(
                    'acs.bookstore'
                )
        return super().create(vals_list)

    ### Payment Invoice
    def payment(self):
        for record in self:
            if not record.book_order_lines:
                raise ValidationError('No books are selected for this order.')

        invoice_lines = []

        for line in record.book_order_lines:
            if not line.book_product:
                raise ValidationError('Book is not selected for one of the lines.')

            invoice_lines.append(
                (
                    0,
                    0,
                    {
                        'product_id': line.book_product.id,
                        'quantity': line.quantity_line,
                        'price_unit': line.price_line,
                    },
                )
            )

        payment_vals = {
            'partner_id': record.customer_name.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': invoice_lines,
        }

        invoice_obj = self.env['account.move'].create(payment_vals)

        self.paid = True
        self._compute_show_pay_button()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice_obj.id,
            'target': 'current',
        }
