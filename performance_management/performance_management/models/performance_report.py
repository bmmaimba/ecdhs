# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PerformanceReport(models.Model):
    _name = 'performance.report'
    _description = 'Performance Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Report Name', required=True, tracking=True)
    programme_id = fields.Many2one('performance.programme', string='Programme')
    report_date = fields.Date(string='Report Date', required=True)
    report_period = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual')
    ], string='Report Period', default='quarterly')
    summary = fields.Text(string='Executive Summary')
    achievements = fields.One2many('performance.achievement', compute='_compute_achievements')

    # Report statistics
    total_indicators = fields.Integer(string='Total Indicators', compute='_compute_report_stats')
    achieved_targets = fields.Integer(string='Achieved Targets', compute='_compute_report_stats')
    overall_performance = fields.Float(string='Overall Performance %', compute='_compute_report_stats')

    @api.depends('programme_id', 'report_date')
    def _compute_achievements(self):
        for record in self:
            if record.programme_id:
                achievements = self.env['performance.achievement'].search([
                    ('indicator_id.programme_id', '=', record.programme_id.id),
                    ('achievement_date', '<=', record.report_date)
                ])
                record.achievements = achievements
            else:
                record.achievements = False

    @api.depends('achievements')
    def _compute_report_stats(self):
        for record in self:
            achievements = record.achievements
            record.total_indicators = len(achievements.mapped('indicator_id'))
            record.achieved_targets = len(achievements.filtered(lambda a: a.percentage_achieved >= 100))

            if achievements:
                record.overall_performance = sum(achievements.mapped('percentage_achieved')) / len(achievements)
            else:
                record.overall_performance = 0.0

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result.message_post(body="Report created successfully")
        return result
