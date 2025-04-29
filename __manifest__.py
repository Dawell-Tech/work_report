{
    'name': 'Work Report',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Manage employee work reports',
    'description': """
This module allows employees to submit work reports and managers to review them.
    """,
    'depends': ['base', 'hr', 'mail'],
    'data': [
    'security/work_report_security.xml',
    'security/ir.model.access.csv',
    'data/employee_work_report_sequence.xml',
    'views/work_report_views.xml',  # Views first
    'views/work_report_menus.xml',  # Then Menus
],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
