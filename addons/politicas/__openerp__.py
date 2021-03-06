# -*- coding: utf-8 -*-
{
    'name': "Tinjaca - Politicas",

    'summary': """
        Definicion de las politicas de financiamiento del FOMDES
    """,

    'description': """
        Tinjaca - Modulo Politicas (FOMDES)
    """,

    'author': "Cooperativa Saní Tecnologías Comunes",
    'website': "http://sani.org.ve",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tinjaca',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','fomdes'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/politicas_views.xml',
        'data/politicas.sectores.csv',
        'data/politicas.tipos_garantia.csv',
        'data/politicas.rubros.csv',
        'data/politicas.documentos_generales.csv',
        'data/politicas.documentos_sector.csv',
        'data/politicas.documentos_garantia.csv',
        'data/politicas.documentos_empresa.csv',
        'data/politicas.forma_pago.csv',
        #'templates.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
