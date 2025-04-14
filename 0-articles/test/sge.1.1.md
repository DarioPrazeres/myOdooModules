Ah, entendi! Se você estiver buscando uma lista de **Classes**, a lógica vai mudar um pouco, porque você precisa lidar com múltiplos resultados e também garantir que os objetos relacionados (como `Periodo` e `AnoLectivo`) sejam preenchidos para todas as classes retornadas.

### 🔄 Refatoração para obter uma lista de Classes

Vamos adaptar o código para pegar várias **Classes** e, ao mesmo tempo, preencher corretamente os objetos relacionados.

### Passos:
1. **Obter as Classes**: A consulta para as `Classes` retorna várias linhas, e vamos preencher uma lista de `Classe`.
2. **Carregar `Periodo` e `AnoLectivo` para cada classe**: Usando uma consulta adicional ou um único _join_.

#### 1. **Consulta para obter lista de `Classes` com `Periodo` e `AnoLectivo`**

```csharp
public List<Classe> ObterClasses()
{
    List<Classe> classes = new List<Classe>();

    using (var connection = new SqlConnection("sua_string_conexao"))
    {
        connection.Open();

        // Consulta para obter todas as classes, junto com Periodo e AnoLectivo
        var sql = @"
            SELECT 
                c.Id, c.Nome, c.PeriodoId, c.AnoLectivoId,
                p.Id AS PeriodoId, p.Nome AS PeriodoNome,
                a.Id AS AnoLectivoId, a.Ano AS AnoLectivoAno
            FROM Classe c
            INNER JOIN Periodo p ON c.PeriodoId = p.Id
            INNER JOIN AnoLectivo a ON c.AnoLectivoId = a.Id";

        // Lê os resultados e mapeia para os objetos
        using (var command = new SqlCommand(sql, connection))
        {
            using (var reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    var classe = new Classe
                    {
                        Id = (int)reader["Id"],
                        Nome = reader["Nome"].ToString(),
                        PeriodoId = (int)reader["PeriodoId"],
                        AnoLectivoId = (int)reader["AnoLectivoId"],
                        Periodo = new Periodo
                        {
                            Id = (int)reader["PeriodoId"],
                            Nome = reader["PeriodoNome"].ToString()
                        },
                        AnoLectivo = new AnoLectivo
                        {
                            Id = (int)reader["AnoLectivoId"],
                            Ano = reader["AnoLectivoAno"].ToString()
                        }
                    };

                    classes.Add(classe);
                }
            }
        }
    }

    return classes;
}
```

---

### ✅ Explicação do que mudou:
1. **SQL com `INNER JOIN`**: Fizemos um `INNER JOIN` para pegar as informações das `Classes`, `Periodos`, e `AnoLectivo` tudo de uma vez.
2. **Preenchendo as entidades**: Para cada linha retornada pelo `ExecuteReader()`, criamos uma instância de `Classe`, `Periodo` e `AnoLectivo`. 
3. **Adicionando na lista**: Cada `Classe` é adicionada à lista `classes`.

Isso elimina a necessidade de fazer várias consultas separadas para cada `Periodo` e `AnoLectivo`, tornando a execução mais eficiente.

### ⚡ Variação: Utilizando o método genérico para listas

Se preferir manter o método genérico, a versão para lista seria assim:

```csharp
public List<Classe> ObterClasses()
{
    List<Classe> classes = new List<Classe>();

    using (var connection = new SqlConnection("sua_string_conexao"))
    {
        connection.Open();

        var sql = @"
            SELECT 
                c.Id, c.Nome, c.PeriodoId, c.AnoLectivoId,
                p.Id AS PeriodoId, p.Nome AS PeriodoNome,
                a.Id AS AnoLectivoId, a.Ano AS AnoLectivoAno
            FROM Classe c
            INNER JOIN Periodo p ON c.PeriodoId = p.Id
            INNER JOIN AnoLectivo a ON c.AnoLectivoId = a.Id";

        classes = ObterEntidades<Classe>(connection, sql, reader => new Classe
        {
            Id = (int)reader["Id"],
            Nome = reader["Nome"].ToString(),
            PeriodoId = (int)reader["PeriodoId"],
            AnoLectivoId = (int)reader["AnoLectivoId"],
            Periodo = new Periodo
            {
                Id = (int)reader["PeriodoId"],
                Nome = reader["PeriodoNome"].ToString()
            },
            AnoLectivo = new AnoLectivo
            {
                Id = (int)reader["AnoLectivoId"],
                Ano = reader["AnoLectivoAno"].ToString()
            }
        });
    }

    return classes;
}

private List<T> ObterEntidades<T>(SqlConnection connection, string sql, Func<SqlDataReader, T> map)
{
    var entidades = new List<T>();

    using (var command = new SqlCommand(sql, connection))
    {
        using (var reader = command.ExecuteReader())
        {
            while (reader.Read())
            {
                entidades.Add(map(reader));
            }
        }
    }

    return entidades;
}
```

### 🧼 Benefícios dessa versão:

- **Menos código repetido**: Não precisa duplicar a lógica de leitura, agora você usa o método genérico `ObterEntidades`.
- **Eficiência**: A consulta para obter tudo junto (com o `JOIN`) é mais eficiente que fazer múltiplas consultas separadas.
- **Flexibilidade**: Se precisar ajustar os dados mapeados ou mudar a consulta, você só precisa alterar um lugar no código.

---

Agora com a lista de `Classes`, você tem um código mais conciso, eficiente e fácil de manter. Se quiser adicionar mais campos ou modificar algo, basta ajustar o mapeamento no `Func<SqlDataReader, T>`. 😉

O que você acha dessa abordagem?