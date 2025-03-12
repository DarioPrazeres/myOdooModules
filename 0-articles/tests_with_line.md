Para testar os modelos em Odoo, você pode criar testes de unidade que validem o comportamento do seu modelo. O Odoo possui um framework de testes baseado no `unittest` do Python. Vou guiar você sobre como escrever testes para os modelos `LibraryLoan` e `LibraryLoanLine`.

### Passo 1: Criar o Arquivo de Teste

Dentro do diretório do seu módulo Odoo, você pode criar uma pasta chamada `tests` (se ainda não existir) e, dentro dela, um arquivo de teste para os seus modelos. Exemplo: `tests/test_library_loan.py`.

Aqui está um exemplo de como você pode estruturar os testes.

### Passo 2: Escrever os Testes

No arquivo de teste, você usará as ferramentas do Odoo para criar dados de teste e validar o comportamento dos modelos. Aqui está um exemplo de como fazer isso:

```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestLibraryLoan(TransactionCase):

    def setUp(self):
        super(TestLibraryLoan, self).setUp()
        # Criando dados de teste necessários
        self.partner = self.env['res.partner'].create({
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        })
        
        self.currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        
        self.book = self.env['library.book'].create({
            'name': 'The Great Gatsby',
            'price_day': 5.0,
            'qty_stock': 10
        })
        
        # Criar um empréstimo
        self.loan = self.env['library.loan'].create({
            'user_id': self.partner.id,
            'currency_id': self.currency.id,
            'price_total': 50.0,
            'ref': 'TEST123'
        })
        
    def test_create_library_loan(self):
        """Testar a criação do modelo de empréstimo"""
        self.assertEqual(self.loan.user_id.name, 'John Doe')
        self.assertEqual(self.loan.price_total, 50.0)
        self.assertEqual(self.loan.ref, 'TEST123')

    def test_create_loan_line(self):
        """Testar a criação de uma linha de empréstimo"""
        loan_line = self.env['library.loan.line'].create({
            'loan_ids': self.loan.id,
            'book_ids': self.book.id,
            'qty': 1,
            'loan_date': '2025-03-12',
            'due_date': '2025-03-19',
            'status': 'loan',
        })
        
        self.assertEqual(loan_line.loan_ids, self.loan)
        self.assertEqual(loan_line.book_ids, self.book)
        self.assertEqual(loan_line.qty, 1)
        self.assertEqual(loan_line.status, 'loan')
        
    def test_total_computation(self):
        """Testar o cálculo do total em library.loan.line"""
        loan_line = self.env['library.loan.line'].create({
            'loan_ids': self.loan.id,
            'book_ids': self.book.id,
            'qty': 2,  # Vamos testar 2 livros
            'loan_date': '2025-03-12',
            'due_date': '2025-03-19',
            'status': 'loan',
        })
        
        # Testar o cálculo do subtotal
        expected_subtotal = 2 * self.book.price_day  # 2 livros * preço por dia
        self.assertEqual(loan_line.sub_total, expected_subtotal)

    def test_invalid_loan(self):
        """Testar se um empréstimo sem um parceiro retorna um erro"""
        with self.assertRaises(ValidationError):
            self.env['library.loan'].create({
                'user_id': False,  # O parceiro é obrigatório
                'currency_id': self.currency.id,
                'price_total': 50.0,
                'ref': 'TESTINVALID'
            })
        
    def test_loan_status_update(self):
        """Testar a atualização de status do empréstimo"""
        loan_line = self.env['library.loan.line'].create({
            'loan_ids': self.loan.id,
            'book_ids': self.book.id,
            'qty': 1,
            'loan_date': '2025-03-12',
            'due_date': '2025-03-19',
            'status': 'loan',
        })
        
        # Atualizar status para 'returned'
        loan_line.status = 'returned'
        self.assertEqual(loan_line.status, 'returned')
        
        # Testar se o status não pode ser 'overdue' antes da data de devolução
        loan_line.status = 'overdue'
        self.assertEqual(loan_line.status, 'overdue')

```

### Passo 3: Explicação do Código de Teste

1. **Criação de Dados de Teste**: Usamos o `setUp` para criar dados que serão reutilizados em diversos testes, como o parceiro (`res.partner`), a moeda (`res.currency`), o livro (`library.book`), e o empréstimo (`library.loan`).

2. **Testar Criação de Empréstimo**: Testamos a criação do modelo de empréstimo (`library.loan`) e validamos se os dados estão sendo armazenados corretamente.

3. **Testar Criação de Linha de Empréstimo**: Testamos a criação do modelo `library.loan.line` e verificamos se a linha do empréstimo está relacionada ao empréstimo e livro corretos.

4. **Testar Cálculo do Subtotal**: Validamos se o valor do `sub_total` da linha de empréstimo está sendo calculado corretamente com base na quantidade de livros.

5. **Testar Erros de Validação**: Criamos um teste para garantir que, se um empréstimo for criado sem um parceiro, ele deve lançar um erro de validação.

6. **Testar Atualização de Status**: Testamos se o status do empréstimo pode ser alterado corretamente e validamos a lógica de status, como mudar para "returned" ou "overdue".

### Passo 4: Executar os Testes

Para rodar os testes, você pode usar o comando do Odoo para testar o módulo:

```bash
$ odoo --test-enable -d nome_do_banco_de_dados
```

Ou você pode rodar os testes diretamente usando o Python, se você estiver no ambiente virtual:

```bash
$ python3 -m unittest discover -s tests
```

### Conclusão

Este é um exemplo básico de como você pode criar testes para seus modelos em Odoo. Você pode expandir esses testes conforme necessário, testando diferentes cenários de comportamento, como valores inválidos, mudanças de estado, e mais.