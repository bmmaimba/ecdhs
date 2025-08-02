# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PerformanceReport(models.Model):
    _name = 'performance.report'
    _description = 'Performance Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Report Name', required=True, tracking=True)
    programme_id = fields.Many2one('performance.programme', string='Programme')
    report_date = fields.Date(string='Report Date', required=True)
    summary = fields.Text(string='Summary')
    achievements = fields.One2many('performance.achievement', compute='_compute_achievements')

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

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result.message_post(body="Report created successfully")
        return result
