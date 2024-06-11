{
    'name': 'Manufacturing Order Extension',
    'summary': 'Add a button to split manufacturing orders',
    'description':
        '''
        This module allows users to split manufacturing orders into multiple smaller orders.
        ''',
    'version': '17.0.1.0.0', 
    'category': 'Manufacturing',
    'depends': [
        'mrp',
    ],
    'data': [
        # SECURITY
        'security/ir.model.access.csv',

        # VIEWS
        'views/mrp_production_form.xml',

        # WIZARD
        'wizard/split_manufacturing_order_wizard.xml',

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
