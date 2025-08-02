# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PerformanceAchievement(models.Model):
    _name = 'performance.achievement'
    _description = 'Performance Achievement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    indicator_id = fields.Many2one('performance.indicator', string='Indicator', required=True)
    actual_value = fields.Float(string='Actual Value', required=True, tracking=True)
    achievement_date = fields.Date(string='Achievement Date', required=True)
    quarter = fields.Selection([
        ('q1', 'Q1 (Apr-Jun)'),
        ('q2', 'Q2 (Jul-Sep)'),
        ('q3', 'Q3 (Oct-Dec)'),
        ('q4', 'Q4 (Jan-Mar)')
    ], string='Quarter', required=True)
    variance = fields.Float(string='Variance', compute='_compute_variance', store=True)
    percentage_achieved = fields.Float(string='% Achieved', compute='_compute_percentage', store=True)
    comments = fields.Text(string='Comments')

    # Related fields for easier reporting
    programme_id = fields.Many2one(related='indicator_id.programme_id', string='Programme', store=True)
    uom_id = fields.Many2one(related='indicator_id.uom_id', string='Unit of Measure', readonly=True)

    # Performance status
    performance_status = fields.Selection([
        ('excellent', 'Excellent (>110%)'),
        ('good', 'Good (100-110%)'),
        ('satisfactory', 'Satisfactory (90-99%)'),
        ('poor', 'Poor (<90%)')
    ], string='Performance Status', compute='_compute_performance_status', store=True)

    @api.depends('actual_value', 'indicator_id', 'quarter')
    def _compute_variance(self):
        for record in self:
            target = self.env['performance.target'].search([
                ('indicator_id', '=', record.indicator_id.id),
                ('quarter', '=', record.quarter)
            ], limit=1)
            if target:
                record.variance = record.actual_value - target.target_value
            else:
                record.variance = 0.0

    @api.depends('actual_value', 'indicator_id', 'quarter')
    def _compute_percentage(self):
        for record in self:
            target = self.env['performance.target'].search([
                ('indicator_id', '=', record.indicator_id.id),
                ('quarter', '=', record.quarter)
            ], limit=1)
            if target and target.target_value:
                record.percentage_achieved = (record.actual_value / target.target_value) * 100
            else:
                record.percentage_achieved = 0.0

    @api.depends('percentage_achieved')
    def _compute_performance_status(self):
        for record in self:
            if record.percentage_achieved >= 110:
                record.performance_status = 'excellent'
            elif record.percentage_achieved >= 100:
                record.performance_status = 'good'
            elif record.percentage_achieved >= 90:
                record.performance_status = 'satisfactory'
            else:
                record.performance_status = 'poor'

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result.message_post(body="Achievement recorded successfully")

        # Auto-update target status if achieved
        target = self.env['performance.target'].search([
            ('indicator_id', '=', result.indicator_id.id),
            ('quarter', '=', result.quarter)
        ], limit=1)
        if target and result.percentage_achieved >= 100:
            target.action_achieve()

        return result
