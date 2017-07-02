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
        'views/backend/menus.xml',
        'views/backend/users.xml',
        'views/backend/belonging.xml',
        'views/backend/offer.xml',
        'views/backend/website.xml',

        'views/frontend/assets.xml',
        'views/frontend/snippets_ppty.xml',

        'security/groups.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

