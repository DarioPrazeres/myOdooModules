Os conceitos básicos de **QWeb** para que você possa criar relatórios PDF mais interessantes no Odoo. O **QWeb** é o motor de template do Odoo que usa sintaxe XML para gerar HTML, PDFs e outros formatos. Ele é amplamente usado para gerar relatórios personalizados no Odoo.

### Estrutura Básica de um Relatório QWeb

Os relatórios QWeb em Odoo são definidos em arquivos XML, e seguem uma estrutura que envolve o layout externo (geralmente chamado de `web.external_layout`) e o conteúdo específico do relatório. Vamos começar com a estrutura básica:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<odoo>
    <data>
        <!-- Definição do Template do Relatório -->
        <template id="nome_do_relatorio">
            <!-- Inclui o layout externo que é usado pela maioria dos relatórios Odoo -->
            <t t-call="web.external_layout">
                <!-- Aqui vai o conteúdo do relatório -->
                <main>
                    <h2>Título do Relatório</h2>
                    <!-- Conteúdo do relatório -->
                </main>
            </t>
        </template>
    </data>
</odoo>
```

### Elementos Essenciais do QWeb

Aqui estão os elementos mais importantes que você pode usar em QWeb:

1. **Expressões Templating (Tags QWeb)**:
   Usamos tags especiais em QWeb para mostrar dados ou controlar o fluxo da lógica.
   
   - `t-field`: Mostra o valor de um campo do banco de dados.
     ```xml
     <span t-field="doc.name"/>
     ```
   - `t-esc`: Escapa o valor de uma expressão (mostra uma string simples).
     ```xml
     <span t-esc="doc.ref"/>
     ```

2. **Laços (`t-foreach`)**:
   Usamos `t-foreach` para iterar sobre listas de registros (por exemplo, linhas de um empréstimo).
   ```xml
   <t t-foreach="doc.loan_line_ids" t-as="line">
       <tr>
           <td><span t-field="line.book_id.name"/></td>
           <td><span t-field="line.return_date"/></td>
           <td><span t-field="line.quantity"/></td>
       </tr>
   </t>
   ```

3. **Condições (`t-if`, `t-else`)**:
   Você pode mostrar ou esconder elementos com base em condições.
   ```xml
   <t t-if="doc.price_total > 100">
       <p>O valor total é maior que 100</p>
   </t>
   <t t-else="">
       <p>O valor total é menor ou igual a 100</p>
   </t>
   ```

4. **Formatação de Data e Moeda**:
   Odoo tem suporte nativo para formatação de datas e valores monetários.
   ```xml
   <!-- Para formatar uma data -->
   <span t-field="doc.date" t-options='{"widget": "date"}'/>
   
   <!-- Para formatar um valor monetário -->
   <span t-field="doc.amount_total" t-options='{"widget": "monetary", "display_currency": doc.currency_id}'/>
   ```

### Criando Relatórios Mais Interessantes

Agora que você conhece os conceitos básicos, vamos avançar para algumas técnicas mais avançadas para melhorar o visual do seu PDF:

#### 1. **Estilos CSS Personalizados**
   Você pode personalizar o estilo do relatório PDF diretamente usando CSS no QWeb:
   
   ```xml
   <style>
       h2 {
           color: #337ab7;
           font-size: 24px;
           text-align: center;
       }
       .table {
           width: 100%;
           border-collapse: collapse;
       }
       .table th, .table td {
           border: 1px solid #ddd;
           padding: 8px;
           text-align: left;
       }
       .table th {
           background-color: #f2f2f2;
       }
   </style>
   ```

#### 2. **Cabeçalhos e Rodapés Personalizados**
   Você pode incluir cabeçalhos e rodapés para tornar o relatório mais profissional. Isso pode ser feito usando a estrutura do layout externo.

   - **Cabeçalho personalizado**:
     ```xml
     <t t-call="web.external_layout_header">
         <div style="text-align: center;">
             <h1>Relatório de Empréstimos</h1>
         </div>
     </t>
     ```

   - **Rodapé personalizado**:
     ```xml
     <t t-call="web.external_layout_footer">
         <div style="text-align: right; font-size: 12px;">
             <p>Página <span t-field="page_number"/> de <span t-field="total_pages"/></p>
         </div>
     </t>
     ```

#### 3. **Exibir Logotipos ou Imagens**
   Você pode adicionar logotipos ou imagens diretamente no relatório:
   
   ```xml
   <img t-att-src="'data:image/png;base64,%s' % (doc.company_id.logo)" style="max-width: 150px;"/>
   ```

#### 4. **Tabelas com Estilo**
   As tabelas são uma parte essencial de relatórios PDF. Aqui está um exemplo de uma tabela bem estilizada para exibir os detalhes de um empréstimo:
   
   ```xml
   <table class="table table-bordered">
       <thead>
           <tr>
               <th>Nome do Livro</th>
               <th>Data de Devolução</th>
               <th>Quantidade</th>
               <th>Preço</th>
           </tr>
       </thead>
       <tbody>
           <t t-foreach="doc.loan_line_ids" t-as="line">
               <tr>
                   <td><span t-field="line.book_id.name"/></td>
                   <td><span t-field="line.return_date" t-options='{"widget": "date"}'/></td>
                   <td><span t-field="line.quantity"/></td>
                   <td><span t-field="line.price" t-options='{"widget": "monetary", "display_currency": doc.currency_id}'/></td>
               </tr>
           </t>
       </tbody>
   </table>
   ```

#### 5. **Quebras de Página e Layout**
   Se o relatório for longo, você pode adicionar quebras de página para evitar que o conteúdo fique muito comprimido:
   
   ```xml
   <div class="pagebreak"></div>
   ```

Você pode também usar colunas, alterar layouts e seções para garantir que o conteúdo seja bem distribuído no relatório.

### Exemplo Completo de Relatório

Aqui está um exemplo completo de um relatório PDF usando as técnicas que discutimos:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<odoo>
    <data>
        <template id="report_loan">
            <t t-call="web.external_layout">
                <main>
                    <h2 style="text-align: center;">Relatório de Empréstimo de Livros</h2>

                    <p><strong>Referência:</strong> <span t-field="doc.ref"/></p>
                    <p><strong>Nome do Cliente:</strong> <span t-field="doc.name_partner"/></p>
                    <p><strong>Total do Empréstimo:</strong> <span t-field="doc.price_total" t-options='{"widget": "monetary", "display_currency": doc.currency_id}'/></p>

                    <h3>Detalhes do Empréstimo</h3>
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Nome do Livro</th>
                                <th>Data de Devolução</th>
                                <th>Quantidade</th>
                                <th>Preço</th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-foreach="doc.loan_line_ids" t-as="line">
                                <tr>
                                    <td><span t-field="line.book_id.name"/></td>
                                    <td><span t-field="line.return_date" t-options='{"widget": "date"}'/></td>
                                    <td><span t-field="line.quantity"/></td>
                                    <td><span t-field="line.price" t-options='{"widget": "monetary", "display_currency": doc.currency_id}'/></td>
                                </tr>
                            </t>
                        </tbody>
                    </table>

                    <div class="pagebreak"></div>

                    <p><strong>Rodapé personalizado:</strong> Este é o rodapé do relatório</p>
                </main>
            </t>
        </template>
    </data>
</odoo>
```

### Conclusão

Agora você tem as ferramentas necessárias para criar relatórios QWeb mais interessantes e personalizados no Odoo. Praticar essas técnicas vai te ajudar a dominar a criação de PDFs com boa aparência e profissionalismo. Se você precisar de mais exemplos ou detalhes, sinta-se à vontade para perguntar!