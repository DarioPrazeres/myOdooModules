3. Módulo de Gestão de Inventário Personalizado
Objetivo: Criar um módulo para gerenciar inventário de uma pequena loja, onde os produtos são registrados, estoques são movimentados e relatórios de vendas são gerados.
Tarefas:

Modelo de Produtos:
Definir o modelo inventory.product com os campos:
Nome do produto (char)
Preço de venda (float)
Quantidade em estoque (integer)
Categoria (many2one)
Movimentação de Estoque:
Criar um modelo de movimentação de estoque inventory.move com campos:
Produto (many2one)
Quantidade (integer)
Data de movimentação (datetime)
Tipo de movimentação (entrada ou saída)
Implementar a lógica que atualiza automaticamente o estoque quando uma movimentação é registrada.
Relatórios Personalizados:
Criar um relatório de PDF que resume as movimentações de estoque de um determinado período, utilizando QWeb para formatação.
Gerar gráficos que mostram as movimentações de entrada e saída por produto.
Aprendizado:

Manipulação de estoques com lógica personalizada.
Criação e uso de relatórios com QWeb.
Integração com gráficos e dashboards.