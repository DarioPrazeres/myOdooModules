Para garantir que o Odoo só suba se todos os testes passarem, você pode implementar uma abordagem que use o framework de testes do Odoo e configure a execução de testes de maneira a bloquear a inicialização da aplicação caso algum teste falhe.

Aqui está um esboço de como você pode fazer isso:

### Passo 1: Organizar seus testes
No Odoo, você pode escrever testes em módulos usando o framework `unittest` do Python. Seus testes geralmente ficam dentro de um diretório chamado `tests`, e são executados no momento em que você sobe o Odoo.

Exemplo de um arquivo de teste:

```python
from odoo.tests import common

class TestMinhaFuncionalidade(common.TransactionCase):
    def test_1(self):
        # Teste que verifica se uma funcionalidade específica está funcionando
        self.assertEqual(1 + 1, 2)
    
    def test_2(self):
        # Outro teste
        self.assertTrue(True)
```

### Passo 2: Implementar um script de verificação de testes
Agora, para garantir que a aplicação só suba se os testes passarem, você pode criar um script que execute os testes antes de iniciar o servidor Odoo. Esse script pode ser implementado da seguinte maneira:

1. **Script de execução dos testes**: Crie um script Python para rodar os testes antes de iniciar o Odoo. Por exemplo:

```python
import os
import subprocess
import sys

def run_tests():
    # Executa os testes no diretório atual onde está o Odoo
    result = subprocess.run(['python3', 'odoo-bin', 'test', '--stop-after-init', '--db-filter=mydb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Verifica se houve falhas
    if result.returncode != 0:
        print("Testes falharam! O Odoo não será iniciado.")
        print(result.stderr.decode())  # Exibe o erro
        sys.exit(1)  # Encerra o script com erro
    else:
        print("Todos os testes passaram. Iniciando o Odoo.")
        return True

def start_odoo():
    # Inicia o Odoo caso os testes passem
    subprocess.run(['python3', 'odoo-bin', 'start'])

if __name__ == '__main__':
    if run_tests():
        start_odoo()
```

### Passo 3: Configuração do ambiente
- **Pré-requisito**: Certifique-se de que seu ambiente esteja configurado corretamente, incluindo as dependências necessárias para o Odoo.
- **Banco de Dados de Teste**: No script de teste acima, o parâmetro `--db-filter=mydb` é utilizado para garantir que os testes sejam executados no banco de dados correto. Certifique-se de que o banco de dados de testes esteja configurado.

### Passo 4: Subir a aplicação
Quando você rodar esse script (por exemplo, `python3 run_odoo_with_tests.py`), ele verificará se os testes passam. Caso contrário, ele interromperá a execução e o Odoo não será iniciado.

### Passo 5: Automatizando o processo com CI/CD
Uma prática comum é integrar esse tipo de teste em uma pipeline de CI/CD (Integração Contínua/Entrega Contínua). Ferramentas como GitLab CI, Jenkins ou GitHub Actions podem ser configuradas para rodar esses testes automaticamente antes de realizar o deploy da aplicação.

Dessa forma, você tem uma garantia extra de que a aplicação só será iniciada ou promovida para produção se todos os testes estiverem passando.

### Conclusão
Ao executar os testes antes de subir o Odoo, você evita que alterações que não passaram nos testes afetem o funcionamento da aplicação. O script proposto pode ser ajustado conforme suas necessidades, mas a ideia básica é garantir que apenas após a verificação de sucesso nos testes o Odoo inicie a aplicação.