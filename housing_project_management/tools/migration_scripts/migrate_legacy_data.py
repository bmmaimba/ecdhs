from odoo import api, SUPERUSER_ID
import csv
import logging

_logger = logging.getLogger(__name__)

def migrate_legacy_data(cr, version):
    """Migrate data from legacy system"""
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        try:
            # Read legacy data
            with open('legacy_data.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Create project
                    project_vals = {
                        'name': row['project_name'],
                        'project_type': row['type'],
                        'budget_allocation': float(row['budget']),
                    }
                    project = env['housing.project'].create(project_vals)

                    # Create beneficiaries
                    beneficiary_vals = {
                        'name': row['beneficiary_name'],
                        'id_number': row['id_number'],
                        'project_id': project.id,
                    }
                    env['housing.beneficiary'].create(beneficiary_vals)

            _logger.info('Legacy data migration completed successfully')

        except Exception as e:
            _logger.error('Error during migration: %s', str(e))
            raise
