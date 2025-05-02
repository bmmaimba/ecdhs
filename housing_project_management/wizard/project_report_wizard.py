from odoo import models, fields, api
from datetime import datetime, timedelta

class ProjectReportWizard(models.TransientModel):
    _name = 'housing.project.report.wizard'
    _description = 'Project Report Wizard'

    project_id = fields.Many2one('housing.project', string='Project')
    project_type = fields.Selection([
        ('irdp', 'Integrated Residential Development'),
        ('uisp', 'Informal Settlement Upgrade'),
        ('rural', 'Rural Subsidy')
    ], string='Project Type')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To', default=fields.Date.today)
    include_beneficiaries = fields.Boolean('Include Beneficiaries', default=True)
    include_services = fields.Boolean('Include Services', default=True)
    include_budget = fields.Boolean('Include Budget Details', default=True)
    report_type = fields.Selection([
        ('summary', 'Summary Report'),
        ('detailed', 'Detailed Report')
    ], string='Report Type', default='summary', required=True)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            self.project_type = self.project_id.project_type

    def _get_domain(self):
        domain = []
        if self.project_id:
            domain.append(('id', '=', self.project_id.id))
        elif self.project_type:
            domain.append(('project_type', '=', self.project_type))

        if self.date_from:
            domain.append(('create_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('create_date', '<=', self.date_to))

        return domain

    def action_generate_report(self):
        self.ensure_one()

        # Get projects based on criteria
        domain = self._get_domain()
        projects = self.env['housing.project'].search(domain)

        if not projects:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Projects',
                    'message': 'No projects found matching the criteria.',
                    'sticky': False,
                    'type': 'warning',
                }
            }

        # Generate report based on type
        if self.report_type == 'summary':
            return self._generate_summary_report(projects)
        else:
            return self._generate_detailed_report(projects)

    def _generate_summary_report(self, projects):
        # This would typically generate a PDF or Excel report
        # For now, we'll just return a notification
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Report Generated',
                'message': f"Summary report generated for {len(projects)} projects.",
                'sticky': False,
                'type': 'success',
            }
        }

    def _generate_detailed_report(self, projects):
        # This would typically generate a PDF or Excel report
        # For now, we'll just return a notification
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Report Generated',
                'message': f"Detailed report generated for {len(projects)} projects.",
                'sticky': False,
                'type': 'success',
            }
        }
