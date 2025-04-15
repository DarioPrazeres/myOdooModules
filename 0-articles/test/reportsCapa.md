Claro! Vamos organizar **tudo em um fluxo completo**, com os três recursos principais:

---

## 🗂️ **Objetivo Geral**

Criar um formulário em C# WinForms com DevExpress que:

1. ✅ **Faz upload de um arquivo** (PDF ou imagem até 5 MB) e salva no banco de dados.
2. 👁️ **Permite visualizar (preview)** o PDF diretamente no `PdfViewer`.
3. 🖨️ **Imprime um relatório (`XtraReport`)**, colocando o PDF do banco como **capa**.

---

## 📦 Estrutura do Projeto

### 🎯 Tabela no banco de dados:
```sql
CREATE TABLE ArquivosPDF (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    NomeArquivo NVARCHAR(255),
    ConteudoArquivo VARBINARY(MAX)
);
```

---

## 🧱 Backend: `PdfRepository.cs`

```csharp
using System;
using System.Data.SqlClient;
using System.IO;
using System.Linq;
using DevExpress.Pdf;
using DevExpress.XtraEditors;
using DevExpress.XtraReports.UI;

public static class PdfRepository
{
    private static readonly string[] ImagensPermitidas = { ".jpg", ".jpeg", ".png", ".gif", ".bmp" };

    public static void SalvarPdfOuImagemNoBanco(string caminhoArquivo, string connectionString)
    {
        try
        {
            if (!File.Exists(caminhoArquivo))
            {
                XtraMessageBox.Show("Arquivo não encontrado!", "Erro", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Error);
                return;
            }

            FileInfo fileInfo = new FileInfo(caminhoArquivo);
            if (fileInfo.Length > 5 * 1024 * 1024)
            {
                XtraMessageBox.Show("Arquivo maior que 5MB!", "Erro", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Error);
                return;
            }

            string ext = Path.GetExtension(caminhoArquivo).ToLower();
            if (ext != ".pdf" && !ImagensPermitidas.Contains(ext))
            {
                XtraMessageBox.Show("Apenas PDF ou imagens são permitidos.", "Erro", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Error);
                return;
            }

            string nomeArquivo = Path.GetFileName(caminhoArquivo);
            byte[] conteudo = File.ReadAllBytes(caminhoArquivo);

            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                string query = "INSERT INTO ArquivosPDF (NomeArquivo, ConteudoArquivo) VALUES (@NomeArquivo, @ConteudoArquivo)";
                using (SqlCommand cmd = new SqlCommand(query, conn))
                {
                    cmd.Parameters.AddWithValue("@NomeArquivo", nomeArquivo);
                    cmd.Parameters.AddWithValue("@ConteudoArquivo", conteudo);
                    cmd.ExecuteNonQuery();
                }
            }

            XtraMessageBox.Show("Arquivo salvo com sucesso!", "Sucesso", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            XtraMessageBox.Show("Erro ao salvar: " + ex.Message);
        }
    }

    public static void VisualizarPdfNoViewer(int id, string connectionString, DevExpress.XtraPdfViewer.PdfViewer pdfViewer)
    {
        try
        {
            byte[] conteudoPdf = RecuperarArquivo(id, connectionString);
            if (conteudoPdf == null)
            {
                XtraMessageBox.Show("Arquivo não encontrado.");
                return;
            }

            using (MemoryStream ms = new MemoryStream(conteudoPdf))
            {
                pdfViewer.LoadDocument(ms);
            }
        }
        catch (Exception ex)
        {
            XtraMessageBox.Show("Erro ao carregar: " + ex.Message);
        }
    }

    public static void ImprimirComCapa(int idCapa, string connectionString, XtraReport relatorio)
    {
        try
        {
            byte[] capaPdf = RecuperarArquivo(idCapa, connectionString);
            if (capaPdf == null)
            {
                XtraMessageBox.Show("Capa não encontrada!");
                return;
            }

            using (MemoryStream capaStream = new MemoryStream(capaPdf))
            {
                PdfDocumentProcessor capaProcessor = new PdfDocumentProcessor();
                capaProcessor.LoadDocument(capaStream);

                MemoryStream relatorioStream = new MemoryStream();
                relatorio.ExportToPdf(relatorioStream);
                relatorioStream.Position = 0;

                PdfDocumentProcessor relatorioProcessor = new PdfDocumentProcessor();
                relatorioProcessor.LoadDocument(relatorioStream);

                capaProcessor.Append(relatorioProcessor);
                capaProcessor.Print();
            }

            XtraMessageBox.Show("Impressão enviada!", "Impressão", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            XtraMessageBox.Show("Erro na impressão: " + ex.Message);
        }
    }

    private static byte[] RecuperarArquivo(int id, string connectionString)
    {
        byte[] conteudo = null;
        using (SqlConnection conn = new SqlConnection(connectionString))
        {
            conn.Open();
            string query = "SELECT ConteudoArquivo FROM ArquivosPDF WHERE Id = @Id";
            using (SqlCommand cmd = new SqlCommand(query, conn))
            {
                cmd.Parameters.AddWithValue("@Id", id);
                using (SqlDataReader reader = cmd.ExecuteReader())
                {
                    if (reader.Read())
                        conteudo = (byte[])reader["ConteudoArquivo"];
                }
            }
        }
        return conteudo;
    }
}
```

---

## 🧾 No seu `XtraForm` (Formulário DevExpress)

### 🎛️ Componentes sugeridos no Designer:
- `PdfViewer` → `pdfViewer1`
- `SimpleButton` → `btnUpload`
- `SimpleButton` → `btnVisualizar`
- `SimpleButton` → `btnImprimir`
- `OpenFileDialog` → `openFileDialog1`
- `TextBox` ou `SpinEdit` → Para informar o ID do arquivo (`txtIdArquivo`)

---

## ⚙️ Código no `XtraForm.cs`

```csharp
string connectionString = "Server=localhost;Database=SeuBanco;User Id=usuario;Password=senha;";

private void btnUpload_Click(object sender, EventArgs e)
{
    openFileDialog1.Title = "Selecione um PDF ou Imagem";
    openFileDialog1.Filter = "PDF e Imagens|*.pdf;*.jpg;*.jpeg;*.png;*.bmp;*.gif";

    if (openFileDialog1.ShowDialog() == DialogResult.OK)
    {
        PdfRepository.SalvarPdfOuImagemNoBanco(openFileDialog1.FileName, connectionString);
    }
}

private void btnVisualizar_Click(object sender, EventArgs e)
{
    if (int.TryParse(txtIdArquivo.Text, out int id))
    {
        PdfRepository.VisualizarPdfNoViewer(id, connectionString, pdfViewer1);
    }
    else
    {
        XtraMessageBox.Show("ID inválido.");
    }
}

private void btnImprimir_Click(object sender, EventArgs e)
{
    if (int.TryParse(txtIdArquivo.Text, out int id))
    {
        XtraReport meuRelatorio = new MeuRelatorio(); // Substitua por seu XtraReport
        PdfRepository.ImprimirComCapa(id, connectionString, meuRelatorio);
    }
    else
    {
        XtraMessageBox.Show("ID inválido.");
    }
}
```

---

## ✅ Fluxo do Usuário

1. **Upload**:
   - Clica em `Upload`
   - Seleciona um PDF ou imagem (<= 5MB)
   - Arquivo salvo no banco de dados

2. **Visualizar**:
   - Informa o `ID` do arquivo
   - Clica em `Visualizar`
   - PDF carregado no `PdfViewer`

3. **Imprimir com capa**:
   - Informa o `ID` da capa
   - Clica em `Imprimir`
   - O relatório é gerado, o PDF da capa é mesclado, e ambos são impressos

---

## 🔚 Observações Finais

- Certifique-se de que o `DevExpress.Pdf` e `XtraReports` estão corretamente referenciados.
- Substitua `MeuRelatorio` pelo seu próprio relatório (`XtraReport`) customizado.
- Você pode usar uma `GridControl` para listar os arquivos disponíveis e facilitar a seleção por ID.

---

Se quiser, posso montar uma versão com `GridControl` e seleção dinâmica. Só falar! Deseja esse próximo passo?