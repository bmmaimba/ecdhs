# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PerformanceIndicator(models.Model):
    _name = 'performance.indicator'
    _description = 'Performance Indicator'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Indicator Name', required=True, tracking=True)
    programme_id = fields.Many2one('performance.programme', string='Programme', required=True)
    output_indicator = fields.Text(string='Output Indicator', tracking=True,
                                  help="Specific output indicator description for this performance indicator")

    # International UoM standards
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True, tracking=True,
                            help="International standard unit of measure")
    uom_category_id = fields.Many2one(related='uom_id.category_id', string='UoM Category', readonly=True)

    baseline = fields.Float(string='Baseline Value')
    targets = fields.One2many('performance.target', 'indicator_id', string='Targets')
    achievements = fields.One2many('performance.achievement', 'indicator_id', string='Achievements')

    # Computed fields for analysis
    latest_achievement = fields.Float(string='Latest Achievement', compute='_compute_latest_achievement')
    performance_trend = fields.Selection([
        ('improving', 'Improving'),
        ('declining', 'Declining'),
        ('stable', 'Stable'),
        ('no_data', 'No Data')
    ], string='Performance Trend', compute='_compute_performance_trend')

    @api.depends('achievements.actual_value', 'achievements.achievement_date')
    def _compute_latest_achievement(self):
        for record in self:
            latest = record.achievements.sorted('achievement_date', reverse=True)
            record.latest_achievement = latest[0].actual_value if latest else 0.0

    @api.depends('achievements.actual_value')
    def _compute_performance_trend(self):
        for record in self:
            achievements = record.achievements.sorted('achievement_date')
            if len(achievements) < 2:
                record.performance_trend = 'no_data'
            else:
                recent = achievements[-2:].mapped('actual_value')
                if recent[1] > recent[0]:
                    record.performance_trend = 'improving'
                elif recent[1] < recent[0]:
                    record.performance_trend = 'declining'
                else:
                    record.performance_trend = 'stable'

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result.message_post(body="Indicator created successfully")
        return result
