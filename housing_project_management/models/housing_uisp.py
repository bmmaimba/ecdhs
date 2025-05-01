from odoo import models, fields, api

class HousingUISP(models.Model):
    _name = 'housing.uisp'
    _description = 'Upgrading of Informal Settlements Programme'
    _inherit = 'housing.project'

    # UISP specific fields
    settlement_name = fields.Char('Settlement Name')
    household_count = fields.Integer('Number of Households')

    # Override project_type default
    project_type = fields.Selection(
        selection_add=[],
        default='uisp'
    )
