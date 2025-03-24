As setas representam os tipos de relacionamentos entre tabelas em bancos de dados e modelagem de entidades em sistemas. Abaixo estão as representações dessas relações:

### 1. **One-to-Many (1:N)**
   - **Significado:** Uma instância de uma entidade está relacionada com muitas instâncias de outra entidade.
   - **Exemplo:** Um **Departamento** pode ter muitos **Funcionários**, mas cada **Funcionário** pertence a um único **Departamento**.
   - **Representação de seta:** 
     - **1 → N**
   - **Seta:** Uma seta simples de um lado (1) apontando para o outro lado (N).

   **Diagrama:** 
   ```
   Departamento ← 1 -------> N Funcionário
   ```

### 2. **Many-to-One (N:1)**
   - **Significado:** Muitas instâncias de uma entidade estão relacionadas com uma única instância de outra entidade.
   - **Exemplo:** Muitos **Funcionários** pertencem a um único **Departamento**.
   - **Representação de seta:** 
     - **N → 1**
   - **Seta:** A seta vai do lado "muitos" (N) para o lado "um" (1).

   **Diagrama:** 
   ```
   Funcionário → N -------> 1 Departamento
   ```

### 3. **Many-to-Many (N:M)**
   - **Significado:** Muitas instâncias de uma entidade podem estar relacionadas com muitas instâncias de outra entidade.
   - **Exemplo:** **Funcionários** podem ser alocados a **Projetos**, e cada **Projeto** pode ter muitos **Funcionários**.
   - **Representação de seta:** 
     - **N ↔ M**
   - **Seta:** As setas vão em ambas as direções entre as duas entidades.

   **Diagrama:**
   ```
   Funcionário ↔ N -------> M Projeto
   ```

### 4. **One-to-One (1:1)**
   - **Significado:** Uma instância de uma entidade está relacionada com uma única instância de outra entidade.
   - **Exemplo:** Cada **Pessoa** tem um **Passaporte**, e cada **Passaporte** pertence a uma única **Pessoa**.
   - **Representação de seta:** 
     - **1 ↔ 1**
   - **Seta:** As setas vão em ambas as direções entre as duas entidades.

   **Diagrama:**
   ```
   Pessoa ↔ 1 -------> 1 Passaporte
   ```

### Resumo das Setas

1. **One-to-Many (1:N)**: **1 → N** (uma entidade em "1" se relaciona com muitas no "N").
2. **Many-to-One (N:1)**: **N → 1** (muitas entidades "N" se relacionam com uma no "1").
3. **Many-to-Many (N:M)**: **N ↔ M** (muitas entidades "N" se relacionam com muitas entidades "M").
4. **One-to-One (1:1)**: **1 ↔ 1** (uma entidade se relaciona com uma única entidade).

Essas setas ajudam a representar as cardinalidades nas relações entre tabelas em bancos de dados relacionais e a modelagem de dados em sistemas.