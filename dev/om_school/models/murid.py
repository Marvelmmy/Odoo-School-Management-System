import num2words
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
import logging 
from num2words import num2words

_logger = logging.getLogger(__name__)

class Murid(models.Model):
    _name = "om_school.murid"  # Model name
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Inherit mail features
    _description = "Student Information"  # Model description
    _rec_name = "nama" 

    # Fields definition
    nama = fields.Char(string="Name", required=True, tracking=True)
    kelas_id = fields.Many2one(
        'om_school.kelas', domain=[], required=True, string='Class'
    )
    alamat = fields.Char(string="Address", required=True, tracking=True)
    no_telp = fields.Char(string="Phone Number", required=True, tracking=True)
    ref = fields.Char(string='Reference', default=lambda self: _('New'))
    is_active = fields.Boolean(string="Status", default=True) 
    bills = fields.One2many('om_school.bills', 'murid_id', string="Bills")
    
    # Generate reference sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', _('New')) == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('om_school.murid') or _('New')
        return super(Murid, self).create(vals_list)

    # Validate phone number
    @api.constrains('no_telp')
    def check_no_telp(self):
        for rec in self:
            if rec.no_telp and not rec.no_telp.isdigit():
                raise ValidationError(_("Phone number must contain digits only!"))

    # Display name with student name
    def name_get(self):
        result = []
        for rec in self:
            display_name = rec.nama or ''
            if rec.kelas_id:
                display_name += f" ({rec.kelas_id.name})"
            result.append((rec.id, display_name))
        return result
    
    # Generate monthly bills
    def generate_monthly_bills(self):
        """Generate monthly bills for students"""
        try:
            if 'om_school.bills' not in self.env:
                _logger.error("Model om_school.bills is not found in registry")
                raise ValueError("Bills model is not properly configured")
            
            for student in self:
                if not student.is_active:
                    continue
                
                current_month = datetime.now().replace(day=1)
                existing_bill = self.env['om_school.bills'].search([
                    ('murid_id', '=', student.id),
                    ('create_date', '>=', current_month),
                    ('create_date', '<', current_month.replace(month=current_month.month + 1) if current_month.month < 12 else current_month.replace(year=current_month.year + 1, month=1))
                ])

                if existing_bill:
                    _logger.info(f"Bill already exists for student {student.nama} for this month")
                    continue 

                bill_name = f"Monthly fee - {student.nama} - {current_month.strftime('%B %Y')}"
                due_date = current_month + timedelta(days=30)

                bills_vals = {
                    'nama': bill_name,
                    'murid_id': student.id,
                    'amount': 500000.0,
                    'due_date': due_date,
                    'state': 'open', 
                    'description': f"Monthly school fee for {current_month.strftime('%B %Y')}"
                }

                new_bill = self.env['om_school.bills'].sudo().create(bills_vals)
                _logger.info(f"Created new bill {new_bill.id} for student {student.nama}")

        except Exception as e:
            _logger.error(f"Error generating monthly bills: {str(e)}")
            raise

    @api.model
    def send_monthly_bills(self):
        """Send bill reminders (placeholder for actual implementation)"""
        _logger.info("Sending monthly bill reminders...")
        pass
    
    
    def action_print_receipt(self):
        self.ensure_one()
        paid_bills = self.env['om_school.bills'].search([
            ('murid_id', '=', self.id),
            ('state', '=', 'paid')
        ])
        if not paid_bills:
            raise UserError("No paid bills found for this student.")
        return self.env.ref('om_school.action_report_murid_payment_done').report_action(paid_bills)



# Bills model 
class MonthlyBills(models.Model):
    _name = "om_school.bills"  # name of the model
    _description = "Monthly bills for student"
    _rec_name = "nama"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # fields definition 
    ref = fields.Char(string='Reference', default=lambda self: _('New'))
    nama = fields.Char(string="Bill Name", required=True, tracking=True)
    murid_id = fields.Many2one('om_school.murid', string='Student', required=True, tracking=True)
    amount = fields.Float(string="Amount", required=True, tracking=True)
    amount_in_words = fields.Char(string="Amount in Words", compute="_compute_amount_in_words", store=False)
    due_date = fields.Date(string="Due Date", required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string="State", default="draft", tracking=True) 
    description = fields.Text(string="Description")
    create_date = fields.Datetime(string="Created On", readonly=True) 
    payment_date = fields.Date(string="Payment Date")

    # Generate reference sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', _('New')) == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('om_school.bills') or _('New')
        return super(MonthlyBills, self).create(vals_list)

    @api.depends('amount')
    def _compute_amount_in_words(self):
        """Compute amount in words"""
        for record in self:
            record.amount_in_words = record._get_amount_in_words(record.amount)

    def action_confirm(self):
        """Confirm the bill"""
        self.state = 'open'
    
    def action_pay(self):
        """Mark as paid"""
        self.state = 'paid'
        self.payment_date = fields.Date.today()

    def action_cancel(self):
        """Cancel the bill"""
        self.state = 'cancelled'
  
    def _compute_amount_in_words(self):
        """Compute amount in words"""
        for record in self:
            record.amount_in_words = record._get_amount_in_words(record.amount)

    def _get_amount_in_words(self, amount):
        """Convert amount to words in Indonesian"""
        return self._simple_amount_to_words(amount)

    def _simple_amount_to_words(self, amount):
        """Simple amount to words converter"""
        if amount == 0:
            return "nol rupiah"
        
        # Simple conversion - extend as needed
        if amount < 1000:
            return f"{int(amount)} rupiah"
        elif amount < 1000000:
            thousands = int(amount // 1000)
            remainder = int(amount % 1000)
            if remainder > 0:
                return f"{thousands} ribu {remainder} rupiah"
            else:
                return f"{thousands} ribu rupiah"
        elif amount < 1000000000:
            millions = int(amount // 1000000)
            remainder = int(amount % 1000000)
            result = f"{millions} juta"
            if remainder >= 1000:
                thousands = int(remainder // 1000)
                result += f" {thousands} ribu"
                remainder = int(remainder % 1000)
            if remainder > 0:
                result += f" {remainder}"
            return result + " rupiah"
        else:
            return f"{int(amount)} rupiah"

    def _compute_total_amount(self):
        """Compute total amount for the bill"""
        for rec in self:
            rec.total_amount = sum(rec.amount for rec in rec.self)
        return rec.total_amount