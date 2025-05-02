from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProjectBudgetAllocationWizard(models.TransientModel):
_name = 'project.budget.allocation.wizard'
_description = 'Project Budget Allocation Wizard'

project_id = fields.Many2one('housing.project', string='Project', required=True)
current_budget = fields.Float(related='project_id.budget_allocation', readonly=True)
additional_budget = fields.Float('Additional Budget', required=True)
reason = fields.Text('Reason for Budget Change', required=True)

def action_allocate_budget(self):
    self.ensure_one()
    if self.additional_budget <= 0:
        raise UserError(_('Additional budget must be positive'))

    self.project_id.write({
        'budget_allocation': self.current_budget + self.additional_budget
    })

    # Create an activity for finance team
    self.env['mail.activity'].create({
        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
        'note': f'Budget increased by {self.additional_budget}. Reason: {self.reason}',
        'res_id': self.project_id.id,
        'res_model_id': self.env['ir.model']._get('housing.project').id,
        'user_id': self.env.user.id,
    })

    return {'type': 'ir.actions.act_window_close'}