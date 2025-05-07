O que você está enfrentando é um comportamento comum no Odoo ao herdar modelos: quando você adiciona campos obrigatórios (`required=True`) diretamente ao modelo base, esses campos serão exigidos **em todos os modelos que o herdam** — o que não é desejado no seu caso.

### ✅ Solução recomendada: **Tornar o campo não obrigatório no modelo base, e validar via `@api.constrains` ou `@api.model` nos filhos**

Vamos usar seu exemplo para mostrar como fazer isso corretamente.

---

### 1. Modelo base `carro.py` (não marca os campos como obrigatórios):

```python
from odoo import models, fields

class Carro(models.Model):
    _name = 'meu.carro'
    _description = 'Carro'

    nome = fields.Char(string='Nome')
    tipo = fields.Selection([
        ('picape', 'Picape'),
        ('suv', 'SUV'),
    ], string='Tipo do carro', required=True)

    tamanho_carroceria = fields.Float(string='Tamanho da carroceria (m)')
    volume_porta_malas = fields.Float(string='Volume do porta-malas (litros)')
```

---

### 2. Submodelo `picape.py` (valida apenas se tipo == picape):

```python
from odoo import models, api, exceptions

class CarroPicape(models.Model):
    _inherit = 'meu.carro'

    @api.constrains('tipo', 'tamanho_carroceria')
    def _check_tamanho_carroceria_picape(self):
        for record in self:
            if record.tipo == 'picape' and not record.tamanho_carroceria:
                raise exceptions.ValidationError("O tamanho da carroceria é obrigatório para picapes.")
```

---

### 3. Submodelo `suv.py` (valida apenas se tipo == suv):

```python
from odoo import models, api, exceptions

class CarroSUV(models.Model):
    _inherit = 'meu.carro'

    @api.constrains('tipo', 'volume_porta_malas')
    def _check_volume_porta_malas_suv(self):
        for record in self:
            if record.tipo == 'suv' and not record.volume_porta_malas:
                raise exceptions.ValidationError("O volume do porta-malas é obrigatório para SUVs.")
```

---

### ✅ Vantagens dessa abordagem:

* O campo **não é globalmente obrigatório**, então pode ser `null` para tipos que não precisam dele.
* A lógica de validação fica **nos modelos apropriados**, e executa apenas quando necessário.
* Você pode fazer validações mais sofisticadas (ex: range, tipos, condições compostas).

Se você quiser também mudar dinamicamente a obrigatoriedade no formulário, posso te mostrar como fazer isso com `@api.onchange` ou `attrs` em XML. Deseja isso também?
