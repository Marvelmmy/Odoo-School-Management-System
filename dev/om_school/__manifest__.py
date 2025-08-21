{
    'name': 'School Management System',
    'version': '16.0.1.0.0',
    'author': 'Marvel Mamuaya',
    'website': 'https://www.schoolSNK.tech',
    'summary': 'Odoo 16 development',
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/guru.xml',
        'views/murid.xml',
        'data/sequence.xml',
    ],
    'description': """
School Management System
==========================
A basic School management system for Odoo 16 to define the relation of student and teacher modul
    """,
    'category': 'Uncategorized',
    'depends': ['base', 'mail', 'sale'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
