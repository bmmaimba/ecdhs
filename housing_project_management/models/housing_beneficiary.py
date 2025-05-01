
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HousingBeneficiary(models.Model):
    _name = 'housing.beneficiary'
    _description = 'Housing Beneficiary'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Beneficiary Name', required=True, tracking=True)
    id_number = fields.Char('ID Number', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    date_of_birth = fields.Date('Date of Birth')
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    address = fields.Text('Address')
    monthly_income = fields.Float('Monthly Income')
    qualification_status = fields.Selection([
        ('qualified', 'Qualified'),
        ('pending', 'Pending Verification'),
        ('disqualified', 'Disqualified')
    ], string='Qualification Status', default='pending', tracking=True)
    vulnerable = fields.Boolean('Vulnerable Household')
    project_id = fields.Many2one('housing.project', string='Project', required=True)
    notes = fields.Text('Notes')

    @api.constrains('id_number')
    def _check_id_number(self):
        for record in self:
            if record.id_number:
                if not record.id_number.isdigit() or len(record.id_number) != 13:
                    raise ValidationError('ID Number must be 13 digits')

    @api.constrains('monthly_income')
    def _check_monthly_income(self):
        for record in self:
            if record.monthly_income < 0:
                raise ValidationError('Monthly income cannot be negative')
