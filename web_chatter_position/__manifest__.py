{
    'name': 'Chatter Position',
    'summary': 'Chatter Position',
    'description': '''
        Configurable Chatter Position.
    ''',
    'version': '17.0.1.0.0', 
    'category': 'Tools/UI',
    'depends': [
        'mail',
    ],
    'data': [
        'views/res_users.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            (
                'after',
                'web/static/src/scss/primary_variables.scss',
                'web_chatter_position/static/src/scss/variables.scss'
            ),
        ],
        'web.assets_backend': [
            (
                'after',
                'mail/static/src/views/web/form/form_compiler.js',
                'web_chatter_position/static/src/views/form/form_compiler.js'
            ),
            'web_chatter_position/static/src/core/**/*.scss',
        ],
    },
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
