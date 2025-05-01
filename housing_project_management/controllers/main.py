from odoo import http
from odoo.http import request
import json

class HousingProjectAPI(http.Controller):
    @http.route('/api/housing/projects', auth='user', type='http', methods=['GET'])
    def get_projects(self, **kwargs):
        projects = request.env['housing.project'].search([])
        result = []
        for project in projects:
            result.append({
                'id': project.id,
                'name': project.name,
                'type': project.project_type,
                'state': project.state,
                'budget': project.budget_allocation,
            })
        return json.dumps(result)

    @http.route('/api/housing/projects/<int:project_id>', auth='user', type='http', methods=['GET'])
    def get_project(self, project_id, **kwargs):
        project = request.env['housing.project'].browse(project_id)
        return json.dumps({
            'id': project.id,
            'name': project.name,
            'type': project.project_type,
            'state': project.state,
            'budget': project.budget_allocation,
            'beneficiaries': len(project.beneficiary_ids),
        })

    @http.route('/api/housing/projects', auth='user', type='json', methods=['POST'])
    def create_project(self, **kwargs):
        vals = request.jsonrequest
        project = request.env['housing.project'].create(vals)
        return {'id': project.id, 'name': project.name}
