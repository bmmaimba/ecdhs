from odoo import models, fields, api

class ProjectApprovalWizard(models.TransientModel):
    _name = 'housing.project.approval.wizard'
    _description = 'Project Approval Wizard'

    project_id = fields.Many2one('housing.project', string='Project', required=True)
    approval_date = fields.Date('Approval Date', default=fields.Date.today, required=True)
    approved_by = fields.Many2one('res.users', string='Approved By', default=lambda self: self.env.user.id, required=True)
    approval_notes = fields.Text('Approval Notes')
    approval_document = fields.Binary('Approval Document')
    approval_filename = fields.Char('Document Filename')

    def action_approve(self):
        self.ensure_one()
        if self.project_id:
            # Create support document for the approval
            if self.approval_document:
                self.env['housing.support'].create({
                    'name': f'Approval Document - {self.project_id.name}',
                    'document_type': 'approval',
                    'project_id': self.project_id.id,
                    'upload_date': self.approval_date,
                    'file_data': self.approval_document,
                    'file_name': self.approval_filename,
                    'notes': self.approval_notes,
                })

            # Update project state based on current state
            if self.project_id.state == 'draft':
                self.project_id.action_start_feasibility()
            elif self.project_id.state == 'feasibility':
                self.project_id.action_start_planning()
            elif self.project_id.state == 'planning':
                self.project_id.action_start_implementation()

            # Log the approval in the chatter
            self.project_id.message_post(
                body=f"Project approved by {self.approved_by.name} on {self.approval_date}. Notes: {self.approval_notes or 'None'}")

        return {'type': 'ir.actions.act_window_close'}
