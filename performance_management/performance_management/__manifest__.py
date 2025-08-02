{
    'name': 'Performance Tracking and Management System',
    'version': '18.0.1.1.0',
    'category': 'Management',
    'summary': 'Track and manage organizational performance indicators and targets with international UoM standards',
    'description': '''
        Performance Tracking and Management System
        ==========================================

        This module provides comprehensive performance tracking capabilities including:
        * Programme management with Outcome Outputs
        * Performance indicators tracking with Output Indicators
        * Target setting and monitoring with quarterly breakdown
        * Achievement recording and analysis with variance calculation
        * Performance reporting and dashboards
        * International Units of Measure (UoM) standards

        Based on Annual Performance Plan 2024/25 requirements.

        Features:
        - Outcome Output tracking per programme
        - Output Indicator specification per performance indicator
        - International UoM standards (SI units, Imperial, etc.)
        - Mail integration for tracking changes
        - Advanced search and filtering
        - Role-based access control
    ''',
    'author': 'Your Organization',
    'website': 'https://www.yourorganization.com',
    'depends': ['base', 'mail', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'data/uom_data.xml',
        'views/performance_menu.xml',
        'views/performance_programme_views.xml',
        'views/performance_indicator_views.xml',
        'views/performance_target_views.xml',
        'views/performance_achievement_views.xml',
        'views/performance_report_views.xml',
        'data/performance_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}