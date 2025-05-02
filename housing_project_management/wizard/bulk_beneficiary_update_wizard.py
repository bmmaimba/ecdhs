from odoo import models, fields, api

class BulkBeneficiaryUpdateWizard(models.TransientModel):
    _name = 'housing.bulk.beneficiary.update.wizard'
    _description = 'Bulk Update Beneficiaries'

    project_id = fields.Many2one('housing.project', string='Project', required=True)
    qualification_status = fields.Selection([
        ('pending', 'Pending'),
        ('qualified', 'Qualified'),
        ('disqualified', 'Disqualified')
    ], string='Qualification Status')
    update_qualification = fields.Boolean('Update Qualification Status')
    update_vulnerable = fields.Boolean('Update Vulnerable Status')
    vulnerable = fields.Boolean('Vulnerable')
    update_notes = fields.Boolean('Add Notes')
    notes = fields.Text('Notes to Add')

    def action_update_beneficiaries(self):
        self.ensure_one()
        if not self.project_id:
            return

        # Get all beneficiaries for the project
        beneficiaries = self.env['housing.beneficiary'].search([
            ('project_id', '=', self.project_id.id)
        ])

        if not beneficiaries:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Beneficiaries',
                    'message': 'No beneficiaries found for this project.',
                    'sticky': False,
                    'type': 'warning',
                }
            }

        # Prepare update values
        update_vals = {}
        if self.update_qualification:
            update_vals['qualification_status'] = self.qualification_status
        if self.update_vulnerable:
            update_vals['vulnerable'] = self.vulnerable

        # Update beneficiaries
        if update_vals:
            beneficiaries.write(update_vals)

        # Add notes if requested
        if self.update_notes and self.notes:
            for beneficiary in beneficiaries:
                new_notes = beneficiary.notes + '\n' + self.notes if beneficiary.notes else self.notes
                beneficiary.write({'notes': new_notes})

                # Log the update in the chatter
                beneficiary.message_post(
                    body=f"Bulk update performed. Notes added: {self.notes}")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Update Successful',
                'message': f"{len(beneficiaries)} beneficiaries updated successfully.",
                'sticky': False,
                'type': 'success',
            }
        }
