from odoo import models, fields, api

class HousingRural(models.Model):
    _name = 'housing.rural'
    _description = 'Rural Subsidy Programme'
    _inherit = 'housing.project'

    # Rural specific fields
    traditional_authority = fields.Char('Traditional Authority')
    land_rights_type = fields.Selection([
        ('communal', 'Communal Land'),
        ('permission', 'Permission to Occupy'),
        ('other', 'Other')
    ], string='Land Rights Type')

    # Override project_type default
    project_type = fields.Selection(
        selection_add=[],
        default='rural'
    )
