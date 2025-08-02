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
        ('q1', 'Q1 (Apr-Jun)'),
        ('q2', 'Q2 (Jul-Sep)'),
        ('q3', 'Q3 (Oct-Dec)'),
        ('q4', 'Q4 (Jan-Mar)')
    ], string='Quarter', required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('achieved', 'Achieved'),
        ('missed', 'Missed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    notes = fields.Text(string='Notes')

    # Related fields for easier reporting
    programme_id = fields.Many2one(related='indicator_id.programme_id', string='Programme', store=True)
    uom_id = fields.Many2one(related='indicator_id.uom_id', string='Unit of Measure', readonly=True)

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result.message_post(body="Target set successfully")
        return result

    def action_activate(self):
        self.status = 'active'
        self.message_post(body="Target activated")

    def action_achieve(self):
        self.status = 'achieved'
        self.message_post(body="Target achieved!")
