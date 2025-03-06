# Módulo de Gestão de Biblioteca
Objetivo: Criar um módulo para gerenciar uma biblioteca, onde os usuários possam cadastrar livros, verificar a disponibilidade e registrar empréstimos e devoluções.

## Tarefas:

### Criação do Módulo:

Estruturar o módulo com os arquivos básicos: 
- __manifest__.py, 
- __init__.py.

### Definir o modelo book.book para gerenciar os livros, com campos como:
- Título (char)
- Autor (many2one - relação com um modelo book.author)
- Categoria (many2one)
- Disponibilidade (boolean)
- Data de publicação (date)
### Definir Views:

- Criar uma view tree (lista) que exibe todos os livros com filtros para "disponível" ou "não disponível".
- Criar um formulário detalhado para editar as informações do livro.
- Fluxo de Empréstimo e Devolução:

### Criar um modelo library.loan para gerenciar os empréstimos, com campos como:
- Livro (many2one, relacionado ao book.book)
- Usuário (many2one, relacionado ao res.users)
- Data de empréstimo (date)
- Data de devolução prevista (date)
- Implementar um botão no formulário de livro para registrar um novo empréstimo.
- Automatizar a Devolução:

- Criar uma ação que marca o livro como "disponível" após a devolução, alterando o estado do livro.

## Aprendizado:

- Definição de modelos, relacionamentos one2many e many2one.
- Criação de views tree e form.
- Utilização de ações e automações.
- Uso de lógica condicional e estados no Odoo.