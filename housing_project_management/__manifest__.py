
{
    'name': 'Housing Project Management',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Manage housing projects including IRDP, UISP, and Rural Subsidy',
    'description': """
        Complete housing project management system for:
        - Integrated Residential Development Programme (IRDP)
        - Upgrading of Informal Settlements Programme (UISP)
        - Rural Subsidy: Communal Land Rights Programme
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base',
        'mail',
        'project',
        'account',
        'survey',
        'web',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/housing_sequence.xml',
        'data/automated_actions.xml',
        'data/scheduled_actions.xml',
        'views/menu.xml',
        'views/housing_project_views.xml',
        'views/housing_irdp_views.xml',
        'views/housing_uisp_views.xml',
        'views/housing_rural_views.xml',
        'views/housing_beneficiary_views.xml',
        'views/housing_services_views.xml',
        'views/housing_support_views.xml',
        'views/housing_dashboard.xml',
        'wizard/project_approval_wizard_view.xml',
        'wizard/beneficiary_import_wizard_view.xml',
        'wizard/project_budget_allocation_wizard_view.xml',
        'wizard/beneficiary_qualification_wizard_view.xml',
        'wizard/bulk_beneficiary_update_wizard_view.xml',
        'wizard/project_report_wizard_view.xml',
        'report/housing_project_analysis.xml',
        'report/project_report_templates.xml',
        'report/project_reports.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'housing_project_management/static/src/js/housing_dashboard.js',
        ],
    },
    'qweb': [
        'static/src/xml/dashboard.xml',
    ],
    'demo': [
        'data/housing_project_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
