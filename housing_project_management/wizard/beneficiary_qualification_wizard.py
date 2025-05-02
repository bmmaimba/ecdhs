from odoo import models, fields, api

class BeneficiaryQualificationWizard(models.TransientModel):
    _name = 'housing.beneficiary.qualification.wizard'
    _description = 'Beneficiary Qualification Wizard'

    beneficiary_id = fields.Many2one('housing.beneficiary', string='Beneficiary', required=True)
    qualification_status = fields.Selection([
        ('pending', 'Pending'),
        ('qualified', 'Qualified'),
        ('disqualified', 'Disqualified')
    ], string='Qualification Status', required=True)
    qualification_date = fields.Date('Qualification Date', default=fields.Date.today, required=True)
    qualified_by = fields.Many2one('res.users', string='Qualified By', default=lambda self: self.env.user.id, required=True)
    qualification_notes = fields.Text('Qualification Notes')
    supporting_document = fields.Binary('Supporting Document')
    document_filename = fields.Char('Document Filename')

    @api.onchange('beneficiary_id')
    def _onchange_beneficiary_id(self):
        if self.beneficiary_id:
            self.qualification_status = self.beneficiary_id.qualification_status

    def action_update_qualification(self):
        self.ensure_one()
        if self.beneficiary_id:
            # Update beneficiary qualification status
            self.beneficiary_id.write({
                'qualification_status': self.qualification_status,
                'notes': self.beneficiary_id.notes + '\n' + self.qualification_notes if self.beneficiary_id.notes else self.qualification_notes
            })

            # Create support document for the qualification
            if self.supporting_document:
                self.env['housing.support'].create({
                    'name': f'Qualification Document - {self.beneficiary_id.name}',
                    'document_type': 'other',
                    'project_id': self.beneficiary_id.project_id.id,
                    'upload_date': self.qualification_date,
                    'file_data': self.supporting_document,
                    'file_name': self.document_filename,
                    'notes': self.qualification_notes,
                })

            # Log the qualification update in the chatter
            self.beneficiary_id.message_post(
                body=f"Qualification status updated to {self.qualification_status} on {self.qualification_date} by {self.qualified_by.name}. Notes: {self.qualification_notes or 'None'}")

        return {'type': 'ir.actions.act_window_close'}
