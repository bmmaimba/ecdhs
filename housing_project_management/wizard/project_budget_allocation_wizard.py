from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectBudgetAllocationWizard(models.TransientModel):
    _name = 'housing.project.budget.allocation.wizard'
    _description = 'Project Budget Allocation Wizard'

    project_id = fields.Many2one('housing.project', string='Project', required=True)
    current_budget = fields.Float('Current Budget', related='project_id.budget_allocation', readonly=True)
    additional_amount = fields.Float('Additional Amount', required=True)
    allocation_date = fields.Date('Allocation Date', default=fields.Date.today, required=True)
    allocated_by = fields.Many2one('res.users', string='Allocated By', default=lambda self: self.env.user.id, required=True)
    allocation_notes = fields.Text('Allocation Notes')
    supporting_document = fields.Binary('Supporting Document')
    document_filename = fields.Char('Document Filename')

    @api.constrains('additional_amount')
    def _check_additional_amount(self):
        for record in self:
            if record.additional_amount <= 0:
                raise ValidationError("Additional amount must be greater than zero.")

    def action_allocate_budget(self):
        self.ensure_one()
        if self.project_id:
            # Update project budget
            new_budget = self.project_id.budget_allocation + self.additional_amount
            self.project_id.write({
                'budget_allocation': new_budget
            })

            # Create support document for the budget allocation
            if self.supporting_document:
                self.env['housing.support'].create({
                    'name': f'Budget Allocation Document - {self.project_id.name}',
                    'document_type': 'other',
                    'project_id': self.project_id.id,
                    'upload_date': self.allocation_date,
                    'file_data': self.supporting_document,
                    'file_name': self.document_filename,
                    'notes': self.allocation_notes,
                })

            # Log the budget allocation in the chatter
            self.project_id.message_post(
                body=f"Budget increased by {self.additional_amount} on {self.allocation_date} by {self.allocated_by.name}. New budget: {new_budget}. Notes: {self.allocation_notes or 'None'}")

        return {'type': 'ir.actions.act_window_close'}
