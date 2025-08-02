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
        ('q1', 'Q1'),
        ('q2', 'Q2'),
        ('q3', 'Q3'),
        ('q4', 'Q4')
    ], string='Quarter', required=True)
    variance = fields.Float(string='Variance', compute='_compute_variance', store=True)
    percentage_achieved = fields.Float(string='% Achieved', compute='_compute_percentage', store=True)
    comments = fields.Text(string='Comments')

    @api.depends('actual_value', 'indicator_id')
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

    @api.depends('actual_value', 'indicator_id')
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

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result.message_post(body="Achievement recorded successfully")
        return result
