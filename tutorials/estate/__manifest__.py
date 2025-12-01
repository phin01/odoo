{
    'name': 'Estate',
    'depends': [
        'base_setup'
    ],

    'application': True,

    'data':[
        'security/ir.model.access.csv',
        
        'views/estate_actions.xml',
        'views/estate_menus.xml',

        'views/estate_property_offer_list.xml',
        
        'views/estate_property_list.xml',
        'views/estate_property_form.xml',
        'views/estate_property_search.xml',

        'views/estate_property_type_form.xml',
    ]
}