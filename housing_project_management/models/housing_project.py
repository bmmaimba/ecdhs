from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class HousingProject(models.Model):
    _name = 'housing.project'
    _description = 'Housing Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char('Project Name', required=True, tracking=True)
    reference = fields.Char('Reference', readonly=True, copy=False)
    project_type = fields.Selection([
        ('irdp', 'Integrated Residential Development'),
        ('uisp', 'Informal Settlement Upgrade'),
        ('rural', 'Rural Subsidy')
    ], required=True, tracking=True)

    # Basic Information
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    municipality_id = fields.Many2one('res.partner', domain=[('is_municipality', '=', True)], tracking=True)
    start_date = fields.Date('Start Date', tracking=True)
    end_date = fields.Date('Expected End Date', tracking=True)
    actual_end_date = fields.Date('Actual End Date', readonly=True, tracking=True)

    # Status and Approvals
    state = fields.Selection([
        ('draft', 'Draft'),
        ('feasibility', 'Feasibility Study'),
        ('planning', 'Planning'),
        ('implementation', 'Implementation'),
        ('completion', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='draft', tracking=True)

    # Financial Information
    budget_allocation = fields.Float('Budget Allocation', tracking=True)
    spent_amount = fields.Float('Spent Amount', compute='_compute_spent_amount', store=True)
    remaining_budget = fields.Float('Remaining Budget', compute='_compute_remaining_budget', store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    # Documents
    feasibility_report = fields.Binary('Feasibility Report')
    feasibility_filename = fields.Char('Feasibility Report Filename')
    environmental_impact = fields.Binary('EIA Report')
    environmental_filename = fields.Char('EIA Report Filename')
    project_description = fields.Text('Project Description')

    # Relationships
    beneficiary_ids = fields.One2many('housing.beneficiary', 'project_id', string='Beneficiaries')
    services_ids = fields.One2many('housing.services', 'project_id', string='Services')
    document_ids = fields.One2many('housing.support', 'project_id', string='Documents')

    @api.model
    def create(self, vals):
        if 'reference' not in vals:
            vals['reference'] = self.env['ir.sequence'].next_by_code('housing.project')
        return super(HousingProject, self).create(vals)
