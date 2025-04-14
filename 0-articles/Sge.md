Boa! Mandaste bem — dá sim pra melhorar bastante aquele primeiro exemplo, tirar repetição e deixar o código mais limpo e reutilizável. Vamos refatorar pra algo mais **DRY** (Don't Repeat Yourself).

### 🔁 Refatorando com um método genérico de leitura

A ideia aqui é ter um método auxiliar que pega uma única linha do banco e converte num objeto do tipo desejado, passando a query e os parâmetros.

---

### ✅ Refatorado: com menos repetição

```csharp
public Classe ObterClasse(int id)
{
    Classe classe = null;

    using (var connection = new SqlConnection("sua_string_conexao"))
    {
        connection.Open();

        classe = ObterEntidade<Classe>(connection,
            "SELECT * FROM Classe WHERE Id = @Id",
            new SqlParameter("@Id", id),
            reader => new Classe
            {
                Id = (int)reader["Id"],
                Nome = reader["Nome"].ToString(),
                PeriodoId = (int)reader["PeriodoId"],
                AnoLectivoId = (int)reader["AnoLectivoId"]
            });

        if (classe != null)
        {
            classe.Periodo = ObterEntidade<Periodo>(connection,
                "SELECT * FROM Periodo WHERE Id = @Id",
                new SqlParameter("@Id", classe.PeriodoId),
                reader => new Periodo
                {
                    Id = (int)reader["Id"],
                    Nome = reader["Nome"].ToString()
                });

            classe.AnoLectivo = ObterEntidade<AnoLectivo>(connection,
                "SELECT * FROM AnoLectivo WHERE Id = @Id",
                new SqlParameter("@Id", classe.AnoLectivoId),
                reader => new AnoLectivo
                {
                    Id = (int)reader["Id"],
                    Ano = reader["Ano"].ToString()
                });
        }
    }

    return classe;
}

private T ObterEntidade<T>(SqlConnection connection, string sql, SqlParameter parametro, Func<SqlDataReader, T> map)
{
    using (var command = new SqlCommand(sql, connection))
    {
        command.Parameters.Add(parametro);

        using (var reader = command.ExecuteReader())
        {
            if (reader.Read())
            {
                return map(reader);
            }
        }
    }

    return default;
}
```

---

### 🧼 Benefícios dessa versão:
- **Menos repetição**: o código pra executar comando e mapear ficou centralizado.
- **Reutilizável**: dá pra usar o `ObterEntidade<T>` em qualquer outro lugar que você precise buscar uma entidade simples por ID.
- **Mais limpo** e fácil de manter.

Se quiser, a gente pode evoluir isso ainda mais pra lidar com listas (`List<T>`), múltiplos parâmetros, etc.

Curte esse estilo ou prefere algo ainda mais enxuto/diferente?