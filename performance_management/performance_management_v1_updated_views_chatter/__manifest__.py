{
    'name': 'Performance Tracking and Management System',
    'version': '18.0.1.0.0',
    'category': 'Management',
    'summary': 'Track and manage organizational performance indicators and targets',
    'description': '''
        Performance Tracking and Management System
        ==========================================

        This module provides comprehensive performance tracking capabilities including:
        * Programme management
        * Performance indicators tracking
        * Target setting and monitoring
        * Achievement recording and analysis
        * Performance reporting and dashboards

        Based on Annual Performance Plan 2024/25 requirements.
    ''',
    'author': 'Your Organization',
    'website': 'https://www.yourorganization.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/performance_menu.xml',
        'views/performance_programme_views.xml',
        'views/performance_indicator_views.xml',
        'views/performance_target_views.xml',
        'views/performance_achievement_views.xml',
        'views/performance_report_views.xml',
        'data/performance_data.xml',
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}