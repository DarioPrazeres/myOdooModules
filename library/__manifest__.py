{
    'name': 'Gestão de Biblioteca',
    'version': '1.0',
    'author': 'Dário Prazeres',
    'description': 'Library for save Books and Register accountability',
    'website': 'www.darioprazeres.com',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/paper_format.xml',
        'views/menu.xml',
        'views/loan.xml',
        'views/loan_line.xml',
        'views/book.xml',
        'views/category.xml',
        'views/author.xml',
        'report/report_loan.xml',
        'report/report.xml',
    ]
}