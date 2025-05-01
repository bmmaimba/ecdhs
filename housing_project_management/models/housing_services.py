
from odoo import models, fields

class HousingServices(models.Model):
    _name = 'housing.services'
    _description = 'Housing Services'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Service Name', required=True)
    type = fields.Selection([
        ('water', 'Water'),
        ('electricity', 'Electricity'),
        ('roads', 'Roads'),
        ('sanitation', 'Sanitation'),
        ('other', 'Other')
    ], string='Service Type', required=True)
    status = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], string='Status', default='planned', tracking=True)
    description = fields.Text('Description')
    project_id = fields.Many2one('housing.project', string='Project', required=True)
    start_date = fields.Date('Start Date')
    completion_date = fields.Date('Completion Date')
    contractor_id = fields.Many2one('res.partner', string='Contractor')
    estimated_cost = fields.Float('Estimated Cost')
    actual_cost = fields.Float('Actual Cost')
    notes = fields.Text('Notes')
