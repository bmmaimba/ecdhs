from odoo import models, fields, api
from odoo.exceptions import UserError

class ProjectApprovalWizard(models.TransientModel):
    _name = 'project.approval.wizard'
    _description = 'Project Approval Wizard'

    project_id = fields.Many2one('housing.project', string='Project', required=True)
    approval_date = fields.Date('Approval Date', default=fields.Date.today)
    notes = fields.Text('Approval Notes')

    def action_approve(self):
        self.ensure_one()
        if not self.project_id:
            raise UserError('Please select a project')

        self.project_id.write({
            'state': 'approved',
        })

        # Log the approval in the chatter
        self.project_id.message_post(
            body=f"Project approved on {self.approval_date}\nNotes: {self.notes or 'N/A'}"
        )

        return {'type': 'ir.actions.act_window_close'}
