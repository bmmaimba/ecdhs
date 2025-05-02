from odoo import models, fields

class HousingSupport(models.Model):
    _name = 'housing.support'
    _description = 'Housing Support Documents'

    name = fields.Char('Document Name', required=True)
    document = fields.Binary('Document')
    filename = fields.Char('Filename')
    project_id = fields.Many2one('housing.project', string='Project', ondelete='cascade')
    upload_date = fields.Date('Upload Date', default=fields.Date.today)
    document_type = fields.Selection([
        ('mec_approval', 'MEC Approval'),
        ('eia', 'Environmental Impact Assessment'),
        ('feasibility', 'Feasibility Study'),
        ('general', 'General'),
    ], string='Document Type', default='general')
    notes = fields.Text('Notes')