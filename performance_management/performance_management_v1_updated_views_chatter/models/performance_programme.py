# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PerformanceProgramme(models.Model):
    _name = 'performance.programme'
    _description = 'Performance Programme'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Programme Name', required=True, tracking=True)
    description = fields.Text(string='Description')
    responsible_user = fields.Many2one('res.users', string='Responsible User', tracking=True)
    indicators = fields.One2many('performance.indicator', 'programme_id', string='Indicators')

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result.message_post(body="Programme created successfully")
        return result
