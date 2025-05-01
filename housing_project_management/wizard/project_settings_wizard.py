from odoo import models, fields, api

class ProjectSettingsWizard(models.TransientModel):
    _name = 'project.settings.wizard'
    _description = 'Housing Project Settings'

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    default_project_duration = fields.Integer('Default Project Duration (months)', default=12)
    minimum_beneficiary_age = fields.Integer('Minimum Beneficiary Age', default=18)
    maximum_income_threshold = fields.Float('Maximum Monthly Income Threshold', default=3500.00)
    enable_auto_approval = fields.Boolean('Enable Automatic Approvals', default=False)
    notification_email = fields.Char('Notification Email')

    @api.model
    def get_settings(self):
        return self.env['ir.config_parameter'].sudo().get_param('housing_project.settings', {})

    def save_settings(self):
        self.ensure_one()
        self.env['ir.config_parameter'].sudo().set_param('housing_project.settings', {
            'default_duration': self.default_project_duration,
            'min_age': self.minimum_beneficiary_age,
            'max_income': self.maximum_income_threshold,
            'auto_approval': self.enable_auto_approval,
            'notification_email': self.notification_email,
        })
        return {'type': 'ir.actions.act_window_close'}
