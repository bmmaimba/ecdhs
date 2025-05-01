from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestHousingProject(TransactionCase):
    def setUp(self):
        super(TestHousingProject, self).setUp()
        self.project_model = self.env['housing.project']
        self.beneficiary_model = self.env['housing.beneficiary']

        # Create test municipality
        self.municipality = self.env['res.partner'].create({
            'name': 'Test Municipality',
            'is_municipality': True,
        })

    def test_project_creation(self):
        """Test project creation and workflow"""
        project = self.project_model.create({
            'name': 'Test Project',
            'project_type': 'irdp',
            'municipality_id': self.municipality.id,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=365),
            'budget_allocation': 1000000,
        })

        self.assertEqual(project.state, 'draft')
        self.assertTrue(project.reference, "Reference should be auto-generated")

    def test_beneficiary_constraints(self):
        """Test beneficiary validation"""
        project = self.project_model.create({
            'name': 'Test Project',
            'project_type': 'irdp',
            'municipality_id': self.municipality.id,
        })

        # Test valid ID number
        beneficiary = self.beneficiary_model.create({
            'name': 'Test Beneficiary',
            'id_number': '8001015009087',
            'project_id': project.id,
        })
        self.assertTrue(beneficiary.id)

        # Test invalid ID number
        with self.assertRaises(ValidationError):
            self.beneficiary_model.create({
                'name': 'Invalid Beneficiary',
                'id_number': '123',  # Invalid ID
                'project_id': project.id,
            })

    def test_project_budget(self):
        """Test budget calculations"""
        project = self.project_model.create({
            'name': 'Budget Test Project',
            'project_type': 'irdp',
            'municipality_id': self.municipality.id,
            'budget_allocation': 1000000,
        })

        self.assertEqual(project.remaining_budget, 1000000)
