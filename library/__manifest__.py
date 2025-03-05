{
    'name': 'Gestão de Biblioteca',
    'version': '1.0',
    'author': 'Dário Prazeres',
    'description': 'Library for save Books and Register accountability',
    'website': 'www.darioprazeres.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/loan.xml',
        'views/menu.xml',
        'views/book.xml',
        'views/category.xml',
        'views/author.xml'
    ]
}