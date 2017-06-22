{
    'name': 'Property management',
    'version': '1.0',
    'category': 'Sales',
    'description': """
Allows for property management in backend
    """,
    'author': 'Mathonet Grégoire',
    'website': "https://mateitright.be/",
    'depends': ['ethereum_contract_odoo'],
    'data': [
        'views/menus.xml',
        'views/users.xml',
        'security/groups.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

