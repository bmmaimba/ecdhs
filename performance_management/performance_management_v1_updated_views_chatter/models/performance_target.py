# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PerformanceTarget(models.Model):
    _name = 'performance.target'
    _description = 'Performance Target'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    indicator_id = fields.Many2one('performance.indicator', string='Indicator', required=True)
    target_value = fields.Float(string='Target Value', required=True, tracking=True)
    target_date = fields.Date(string='Target Date', required=True)
    quarter = fields.Selection([
        ('q1', 'Q1'),
        ('q2', 'Q2'),
        ('q3', 'Q3'),
        ('q4', 'Q4')
    ], string='Quarter', required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('achieved', 'Achieved'),
        ('missed', 'Missed')
    ], string='Status', default='draft', tracking=True)
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result.message_post(body="Target set successfully")
        return result
