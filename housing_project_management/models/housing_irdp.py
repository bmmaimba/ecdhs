from odoo import models, fields, api

class HousingIRDP(models.Model):
    _name = 'housing.irdp'
    _description = 'Integrated Residential Development Programme'
    _inherit = 'housing.project'

    # IRDP specific fields
    phase_count = fields.Integer('Number of Phases', default=1)
    land_availability = fields.Selection([
        ('available', 'Available'),
        ('pending', 'Pending Acquisition'),
        ('not_available', 'Not Available')
    ], string='Land Availability Status')

    # Override project_type default
    project_type = fields.Selection(
        selection_add=[],
        default='irdp'
    )
