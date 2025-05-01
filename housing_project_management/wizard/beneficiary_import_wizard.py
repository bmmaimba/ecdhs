from odoo import models, fields
import base64
import csv
import io

class BeneficiaryImportWizard(models.TransientModel):
    _name = 'beneficiary.import.wizard'
    _description = 'Import Beneficiaries'

    project_id = fields.Many2one('housing.project', string='Project', required=True)
    data_file = fields.Binary('CSV File', required=True)
    filename = fields.Char('Filename')

    def action_import(self):
        if not self.data_file:
            return

        csv_data = base64.b64decode(self.data_file)
        csv_file = io.StringIO(csv_data.decode("utf-8"))
        reader = csv.DictReader(csv_file)

        for row in reader:
            self.env['housing.beneficiary'].create({
                'name': row.get('name'),
                'id_number': row.get('id_number'),
                'monthly_income': float(row.get('monthly_income', 0)),
                'project_id': self.project_id.id,
            })

        return {'type': 'ir.actions.act_window_close'}
