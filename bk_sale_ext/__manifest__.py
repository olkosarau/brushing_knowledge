{
    'name': 'Sale Order Extension',
    'summary': 'Module modernization',
    'description':
        '''
        ''',
    'version': '17.0.1.0.0', 
    'category': 'Sales/Sales',
    'depends': [
        'sale',
        'stock'
    ],
    'data': [
        # SECURITY
        'security/ir.model.access.csv',

        # VIEWS
        'views/sale_order_line_views.xml',

        # WIZARDS

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
