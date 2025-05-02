from odoo import models, fields

class HousingSupport(models.Model):
    _name = 'housing.support'
    _description = 'Housing Support Documents'

    name = fields.Char('Document Name', required=True)
    document_type = fields.Selection([
        ('feasibility', 'Feasibility Study'),
        ('environmental', 'Environmental Assessment'),
        ('approval', 'Approval Document'),
        ('plan', 'Project Plan'),
        ('report', 'Progress Report'),
        ('other', 'Other')
    ], string='Document Type', required=True)
    project_id = fields.Many2one('housing.project', string='Project', required=True)
    upload_date = fields.Date('Upload Date', default=fields.Date.today)
    file_data = fields.Binary('File')
    file_name = fields.Char('File Name')
    notes = fields.Text('Notes')
