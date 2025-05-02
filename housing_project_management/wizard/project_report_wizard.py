from odoo import models, fields, api
from datetime import datetime, timedelta

class ProjectReportWizard(models.TransientModel):
_name = 'project.report.wizard'
_description = 'Project Report Generator'

date_from = fields.Date('Date From')
date_to = fields.Date('Date To')
project_type = fields.Selection([
    ('irdp', 'IRDP'),
    ('uisp', 'UISP'),
    ('rural', 'Rural')
], string='Project Type')
include_beneficiaries = fields.Boolean('Include Beneficiaries')
include_services = fields.Boolean('Include Services')
include_financials = fields.Boolean('Include Financial Details')

def action_generate_report(self):
    domain = []
    if self.date_from:
        domain.append(('create_date', '>=', self.date_from))
    if self.date_to:
        domain.append(('create_date', '<=', self.date_to))
    if self.project_type:
        domain.append(('project_type', '=', self.project_type))

    projects = self.env['housing.project'].search(domain)

    data = {
        'projects': projects.ids,
        'include_beneficiaries': self.include_beneficiaries,
        'include_services': self.include_services,
        'include_financials': self.include_financials,
    }

    return self.env.ref('housing_project_management.action_report_housing_project_detailed').report_action(self, data=data)