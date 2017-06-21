{
    'name': 'Ethereum Contracts',
    'version': '1.0',
    'category': 'Website',
    'description': """
Track contracts on website
    """,
    'author': 'Mathonet Grégoire',
    'website': "https://mateitright.be/",
    'depends': ['website', 'sale', 'crm'],
    'data': [
        'views/backend/users.xml',
        'views/backend/website.xml',
        'views/backend/contract.xml',
        'views/frontend/snippets_will.xml',
        'views/frontend/assets.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

