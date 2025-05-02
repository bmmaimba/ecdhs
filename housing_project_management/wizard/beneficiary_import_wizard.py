from odoo import models, fields, api
import base64
import csv
import io

class BeneficiaryImportWizard(models.TransientModel):
    _name = 'housing.beneficiary.import.wizard'
    _description = 'Import Beneficiaries from CSV'

    project_id = fields.Many2one('housing.project', string='Project', required=True)
    csv_file = fields.Binary('CSV File', required=True)
    filename = fields.Char('Filename')
    delimiter = fields.Selection([
        (',', 'Comma (,)'),
        (';', 'Semicolon (;)'),
        ('\t', 'Tab (\t)')
    ], string='Delimiter', default=',', required=True)

    def action_import(self):
        self.ensure_one()
        if not self.csv_file:
            return

        # Decode the file content
        csv_data = base64.b64decode(self.csv_file)
        csv_file = io.StringIO(csv_data.decode('utf-8'))

        # Read the CSV file
        reader = csv.DictReader(csv_file, delimiter=self.delimiter)

        # Map CSV headers to model fields
        field_mapping = {
            'name': 'name',
            'id_number': 'id_number',
            'gender': 'gender',
            'date_of_birth': 'date_of_birth',
            'phone': 'phone',
            'email': 'email',
            'address': 'address',
            'monthly_income': 'monthly_income',
            'vulnerable': 'vulnerable',
            'notes': 'notes'
        }

        # Create beneficiaries
        beneficiaries_created = 0
        for row in reader:
            beneficiary_vals = {'project_id': self.project_id.id}

            for csv_field, model_field in field_mapping.items():
                if csv_field in row:
                    # Handle special field conversions
                    if model_field == 'monthly_income':
                        try:
                            beneficiary_vals[model_field] = float(row[csv_field])
                        except (ValueError, TypeError):
                            beneficiary_vals[model_field] = 0.0
                    elif model_field == 'vulnerable':
                        beneficiary_vals[model_field] = row[csv_field].lower() in ['true', 'yes', '1']
                    else:
                        beneficiary_vals[model_field] = row[csv_field]

            # Create the beneficiary if we have at least a name
            if 'name' in beneficiary_vals and beneficiary_vals['name']:
                self.env['housing.beneficiary'].create(beneficiary_vals)
                beneficiaries_created += 1

        # Log the import in the project chatter
        self.project_id.message_post(
            body=f"{beneficiaries_created} beneficiaries imported successfully.")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Import Successful',
                'message': f"{beneficiaries_created} beneficiaries imported successfully.",
                'sticky': False,
                'type': 'success',
            }
        }
