# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PerformanceIndicator(models.Model):
    _name = 'performance.indicator'
    _description = 'Performance Indicator'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Indicator Name', required=True, tracking=True)
    programme_id = fields.Many2one('performance.programme', string='Programme', required=True)
    unit_of_measure = fields.Char(string='Unit of Measure', required=True)
    baseline = fields.Float(string='Baseline Value')
    targets = fields.One2many('performance.target', 'indicator_id', string='Targets')
    achievements = fields.One2many('performance.achievement', 'indicator_id', string='Achievements')

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result.message_post(body="Indicator created successfully")
        return result
