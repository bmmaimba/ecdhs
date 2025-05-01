from odoo import api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)

def cleanup_old_data(cr, version):
    """Clean up old/invalid data"""
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Clean up completed projects older than 5 years
        old_projects = env['housing.project'].search([
            ('state', '=', 'completed'),
            ('actual_end_date', '<', fields.Date.today() - relativedelta(years=5))
        ])
        old_projects.unlink()

        # Archive inactive beneficiaries
        inactive_beneficiaries = env['housing.beneficiary'].search([
            ('qualification_status', '=', 'disqualified'),
            ('write_date', '<', fields.Date.today() - relativedelta(months=6))
        ])
        inactive_beneficiaries.write({'active': False})

        _logger.info('Data cleanup completed successfully')
