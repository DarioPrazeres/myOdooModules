2. Módulo de Gerenciamento de Eventos
Objetivo: Desenvolver um módulo que permite gerenciar eventos, com inscrição de participantes e controle de presença.
Tarefas:

Criação do Modelo de Evento:
Definir o modelo event.event com os campos:
Nome do evento (char)
Data e hora (datetime)
Localização (char)
Descrição (text)
Modelo de Participantes:
Criar o modelo event.participant, com os seguintes campos:
Evento (many2one, relacionado ao event.event)
Participante (many2one, relacionado ao res.partner)
Status da inscrição (selection, com opções: "Confirmado", "Pendente", "Cancelado")
Validação de Inscrições:
Criar uma ação server-side que impede a inscrição de mais participantes quando o evento atingir a capacidade máxima.
Dashboard de Eventos:
Criar um dashboard customizado que exibe gráficos com o número de participantes confirmados e o status dos eventos.
Aprendizado:

Uso de relacionamentos complexos com many2one e one2many.
Validações de negócios e restrições.
Personalização de views e criação de gráficos.
Implementação de lógicas de backend e ações automáticas.