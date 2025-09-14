{
    'name': 'KPI Manager Pro - Sistema Profesional de Gestión de Indicadores',
    'version': '17.0.2.0.0',
    'category': 'Business Intelligence/Project Management',
    'summary': 'Sistema avanzado de KPIs con dashboard interactivo, reportes y analytics',
    'description': """
KPI Manager Pro - La Solución Completa para Gestión de Indicadores

Características Premium:
• Dashboard interactivo con gráficos en tiempo real
• Sistema de alertas inteligentes por email
• Reportes profesionales PDF/Excel personalizables
• Métricas avanzadas con análisis predictivo
• Integración con Odoo nativo
• Multi-empresa y multi-idioma
• Soporte para dispositivos móviles
""",
    'author': 'Business Intelligence Solutions',
    'website': 'https://www.bisolutions.com',
    'support': 'soporte@bisolutions.com',
    'depends': ['base', 'web', 'mail'],  # ← REMOVED 'project'
    'data': [
        'security/security.xml',
        'data/email_templates.xml',
        'data/demo_data.xml',
        'views/kpi_views.xml',
        'views/dashboard_views.xml',
        'views/alert_views.xml',
        'reports/kpi_project_report.xml',
        'wizard/export_wizard.xml',
    ],
    'demo': ['data/demo_data.xml'],
    'assets': {
        'web.assets_backend': [
            'kpi_project_evaluation/static/src/css/dashboard.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
    'price': 499.00,
    'currency': 'USD',
}