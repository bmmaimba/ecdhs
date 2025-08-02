# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PerformanceProgramme(models.Model):
    _name = 'performance.programme'
    _description = 'Performance Programme'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Programme Name', required=True, tracking=True)
    description = fields.Text(string='Description')
    outcome_output = fields.Text(string='Outcome Output', tracking=True, 
                                help="Define the expected outcome and output for this programme")
    responsible_user = fields.Many2one('res.users', string='Responsible User', tracking=True)
    indicators = fields.One2many('performance.indicator', 'programme_id', string='Indicators')

    # Computed fields for dashboard
    total_indicators = fields.Integer(string='Total Indicators', compute='_compute_indicators_count')
    active_targets = fields.Integer(string='Active Targets', compute='_compute_targets_count')

    @api.depends('indicators')
    def _compute_indicators_count(self):
        for record in self:
            record.total_indicators = len(record.indicators)

    @api.depends('indicators.targets')
    def _compute_targets_count(self):
        for record in self:
            active_targets = self.env['performance.target'].search_count([
                ('indicator_id.programme_id', '=', record.id),
                ('status', '=', 'active')
            ])
            record.active_targets = active_targets

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result.message_post(body="Programme created successfully")
        return result
