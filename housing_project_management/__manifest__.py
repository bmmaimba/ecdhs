{
    'name': 'Housing Project Management',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Manage housing projects for IRDP, UISP, and Rural programs',
    'description': """
Housing Project Management
==========================
This module provides comprehensive management of housing projects for:
- Integrated Residential Development Programme (IRDP)
- Upgrading of Informal Settlements Programme (UISP)
- Rural Subsidy: Communal Land Rights

Features include:
- Project planning and tracking
- Beneficiary management
- Service delivery tracking
- Document management
- Compliance monitoring
- Reporting and analytics
""",
    'author': 'Eastern Cape Department of Human Settlements',
    'website': 'https://www.ecdhs.gov.za',
    'depends': ['base', 'mail', 'web'],
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',

        # Data
        # 'data/housing_sequence.xml',
        # 'data/automated_actions.xml',

        # Views
        'views/housing_project_views.xml',
        'views/menu.xml',

        # Wizards
        'wizard/project_approval_wizard_view.xml',
        'wizard/beneficiary_import_wizard_view.xml',
        'wizard/project_settings_wizard_view.xml',

        # Reports
        'report/housing_project_analysis.xml',
        'report/project_reports.xml',
        'report/project_report_templates.xml',
    ],
    'demo': [
        'demo/housing_project_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'housing_project_management/static/src/js/housing_dashboard.js',
            'housing_project_management/static/src/xml/dashboard.xml',
        ],
    },
    'license': 'LGPL-3',
}
