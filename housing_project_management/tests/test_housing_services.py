from odoo.tests.common import TransactionCase

class TestHousingServices(TransactionCase):
    def setUp(self):
        super(TestHousingServices, self).setUp()
        self.service_model = self.env['housing.services']
        self.project_model = self.env['housing.project']

        # Create test project
        self.project = self.project_model.create({
            'name': 'Service Test Project',
            'project_type': 'irdp',
        })

    def test_service_creation(self):
        """Test service creation and status updates"""
        service = self.service_model.create({
            'name': 'Water Service',
            'type': 'water',
            'project_id': self.project.id,
        })

        self.assertEqual(service.status, 'planned')

        # Test status change
        service.write({'status': 'in_progress'})
        self.assertEqual(service.status, 'in_progress')
