{
    'name': 'Estate',
    'depends': [
        'base_setup'
    ],

    'application': True,

    'data':[
        'security/ir.model.access.csv',
        
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_list.xml',
        'views/estate_form.xml'
    ]
}