from odoo import models, fields, tools

class ProjectPerformanceReport(models.Model):
    _name = 'housing.project.performance.report'
    _description = 'Project Performance Analysis'
    _auto = False
    _order = 'date desc'

    date = fields.Date('Date')
    project_id = fields.Many2one('housing.project', string='Project')
    project_type = fields.Selection(related='project_id.project_type')
    municipality_id = fields.Many2one('res.partner', string='Municipality')
    beneficiary_count = fields.Integer('Beneficiaries')
    budget_allocation = fields.Float('Budget')
    budget_spent = fields.Float('Spent')
    completion_rate = fields.Float('Completion Rate (%)')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE or REPLACE VIEW %s as (
                SELECT
                    p.id as id,
                    p.start_date as date,
                    p.id as project_id,
                    p.project_type as project_type,
                    p.municipality_id as municipality_id,
                    COUNT(b.id) as beneficiary_count,
                    p.budget_allocation as budget_allocation,
                    p.spent_amount as budget_spent,
                    CASE 
                        WHEN p.budget_allocation > 0 
                        THEN (p.spent_amount / p.budget_allocation) * 100 
                        ELSE 0 
                    END as completion_rate
                FROM housing_project p
                LEFT JOIN housing_beneficiary b ON b.project_id = p.id
                GROUP BY p.id, p.start_date, p.project_type, 
                         p.municipality_id, p.budget_allocation, p.spent_amount
            )
        """ % self._table)