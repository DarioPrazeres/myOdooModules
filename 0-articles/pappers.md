Ah, entendi! Você quer aprender sobre o formato de documentos (papers) especificamente no **Odoo**.

No Odoo, você pode gerar diferentes tipos de relatórios ou documentos formatados para uso em empresas (como faturas, orçamentos, relatórios de vendas etc.), mas se você estiver se referindo ao desenvolvimento ou personalização de relatórios, posso te orientar em como configurar ou formatar documentos no Odoo.

Vamos nos concentrar em dois cenários comuns:

### 1. **Customização de Relatórios em PDF (QWeb Reports)**
O Odoo usa **QWeb**, que é um mecanismo de renderização baseado em XML, para criar relatórios e documentos (como faturas, orçamentos, etc.) em formato PDF. Você pode personalizar esses relatórios de várias formas, como alterando o layout, cabeçalhos, rodapés e o conteúdo principal.

#### Passos básicos para personalizar um relatório QWeb:

1. **Acessar o Módulo de Relatórios:**
   - Vá até **Configurações** → **Técnico** → **Relatórios** para acessar os relatórios gerados em QWeb.
   - Encontre o relatório que deseja personalizar (por exemplo, o relatório de fatura).

2. **Encontrar a Visualização QWeb:**
   - Cada relatório possui uma ou mais **visualizações QWeb** associadas a ele. Essas visualizações são o que controlam o layout e a estrutura do relatório.
   - As visualizações QWeb podem ser acessadas em **Configurações** → **Técnico** → **Visualizações**.

3. **Editar o Template XML:**
   - Depois de encontrar a visualização QWeb associada ao relatório, você pode editar o **código XML** para alterar o layout. O XML define como o relatório será renderizado em PDF, como as tabelas, logos, textos, etc.
   
   - Por exemplo, se você deseja mudar o logo de uma fatura ou alterar o rodapé, você editaria as tags `<div>`, `<table>`, `<t>` e outros elementos HTML dentro do XML.

   Aqui está um exemplo de como uma parte de um relatório de fatura pode parecer em QWeb:
   ```xml
   <t t-name="account.report_invoice_document">
       <div class="page">
           <h2>Invoice</h2>
           <table class="table">
               <tr>
                   <td>Invoice Date</td>
                   <td><span t-field="o.date_invoice"/></td>
               </tr>
               <tr>
                   <td>Customer</td>
                   <td><span t-field="o.partner_id.name"/></td>
               </tr>
           </table>
       </div>
   </t>
   ```

   Neste código, `<t t-name="account.report_invoice_document">` define o modelo. Os elementos dentro das tags QWeb (como `<span t-field="o.date_invoice"/>`) puxam dados do objeto Odoo (neste caso, a data da fatura e o nome do cliente).

4. **Testar e Visualizar:**
   - Depois de salvar as mudanças no QWeb, você pode gerar um PDF (por exemplo, emitir uma fatura) para ver como o novo layout aparece.

### 2. **Criando um Novo Relatório**
Se você quiser criar um **novo relatório** do zero, siga estas etapas:

1. **Definir a Estrutura do Relatório:**
   - Primeiro, crie um novo template QWeb com a estrutura que você deseja.
   - Vá para **Configurações** → **Técnico** → **Visualizações** e clique em "Criar" para adicionar um novo template XML.

2. **Vincular o Template ao Relatório:**
   - Depois de criar o template XML, vá para **Configurações** → **Técnico** → **Relatórios**.
   - Clique em "Criar" para adicionar um novo relatório e vincule o novo template QWeb que você criou.

3. **Especificar o Modelo de Dados:**
   - Especifique qual **modelo** de dados será usado para o relatório. Por exemplo, se for um relatório de fatura, você deve vincular o modelo `account.move`.

4. **Configurar as Opções de PDF:**
   - O Odoo usa **wkhtmltopdf** para gerar PDFs. Você pode configurar margens, cabeçalhos, rodapés e outras opções específicas para renderização PDF no arquivo XML.

### 3. **Dicas para Personalizar Relatórios QWeb:**
   - **Elementos HTML:** QWeb é baseado em HTML e XML, então, use tags HTML padrão, como `<table>`, `<div>`, `<span>`, etc.
   - **CSS:** Você pode estilizar seus relatórios usando CSS diretamente no QWeb ou adicionar classes CSS customizadas.
   - **QWeb Directives:** Existem algumas diretivas especiais que você usará em QWeb, como:
     - `<t t-field="obj.field_name"/>` para exibir valores de campos.
     - `<t t-if="condition">` para condicionalmente exibir ou ocultar partes do relatório.
   - **Tradução:** Se você precisar que o relatório seja exibido em diferentes idiomas, pode usar o mecanismo de tradução de QWeb com `<t t-esc="obj.field_name" t-options="{'lang': 'en'}"/>`.

### Exemplo de Template QWeb Completo:
```xml
<t t-name="custom_module.report_custom_document">
    <div class="page">
        <h1>My Custom Report</h1>
        <p>Date: <span t-field="o.create_date"/></p>
        <p>Customer: <span t-field="o.partner_id.name"/></p>

        <table class="table">
            <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Price</th>
            </tr>
            <t t-foreach="o.order_line" t-as="line">
                <tr>
                    <td><span t-field="line.product_id.name"/></td>
                    <td><span t-field="line.product_uom_qty"/></td>
                    <td><span t-field="line.price_unit"/></td>
                </tr>
            </t>
        </table>
    </div>
</t>
```

Esse código renderiza um relatório com informações do pedido (data de criação, cliente, linhas de produtos).

### Recursos Adicionais:
- Você pode usar o **Odoo Studio** (se disponível) para facilitar a criação e personalização de relatórios, sem precisar editar diretamente o XML.
- Use o **módulo de relatórios** para configurar permissões e opções avançadas de impressão.

Se você precisar de ajuda para um relatório específico ou um layout que deseja criar, posso te ajudar com exemplos mais detalhados!