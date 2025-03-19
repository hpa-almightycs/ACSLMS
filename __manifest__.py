{
    'name': 'Library Management System',
    'version': '1.0.1',
    'license': 'LGPL-3',  
    'summary': 'ACS Library Management System to manage library',
    'author': 'ACS',
    'category': 'Library',
    'depends': ['base','account','hr','product'],  
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        
        'data/seq.xml',
        
        'views/bookstore_view.xml',
        'views/member_view.xml',
        'views/staff_view.xml',
        'views/author_view.xml',
        'views/menu_view.xml',
        
        'reports/lms_report.xml',  
        
        'wizards/wizard_view.xml',  
    ],
    'demo':[
       
    ]
  

}
