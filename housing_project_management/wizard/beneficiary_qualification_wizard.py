from odoo import models, fields, api

class BeneficiaryQualificationWizard(models.TransientModel):
_name = 'beneficiary.qualification.wizard'
_description = 'Beneficiary Qualification Wizard'

beneficiary_ids = fields.Many2many('housing.beneficiary', string='Beneficiaries')
qualification_status = fields.Selection([
    ('qualified', 'Qualified'),
    ('pending', 'Pending Verification'),
    ('disqualified', 'Disqualified')
], string='Qualification Status', required=True)
notes = fields.Text('Notes')

def action_update_qualification(self):
    self.ensure_one()
    self.beneficiary_ids.write({
        'qualification_status': self.qualification_status,
    })
    if self.notes:
        for beneficiary in self.beneficiary_ids:
            beneficiary.message_post(body=self.notes)
    return {'type': 'ir.actions.act_window_close'}