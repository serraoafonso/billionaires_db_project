# AGENTS.md — Regras do Projeto (CC2005 · Billionaires DB)

Este ficheiro define as convenções do repositório para todos os membros do grupo (Pessoas 1 a 4) e para qualquer assistente de IA usado durante o desenvolvimento.

---

## 1. Regra de Ouro: Código Simples e Legível para Humanos

Todo o código (Python, SQL, HTML e CSS) **tem de ser o mais simples, direto e percetível possível para um humano** — qualquer elemento do grupo deve conseguir lê-lo e explicá-lo facilmente na apresentação oral ao professor.

- **Sem over-engineering**: evitar abstrações desnecessárias, classes complexas, ORMs, metaprogramação, geradores mágicos de rotas/SQL ou bibliotecas externas que não sejam estritamente necessárias.
- **Estilo explícito e didático**: preferir código óbvio e legível a código "esperto" ou demasiado compacto.
- **SQL limpo e indentado**: escrever cada cláusula (`SELECT`, `FROM`, `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`) na sua linha, com aliases curtos e claros.
- **Nomes descritivos**: tabelas e colunas em `snake_case`, em inglês ou português consistente (sem acentos, espaços nem caracteres especiais).
- **Comentários úteis**: comentários breves apenas para explicar o contexto ou decisões importantes; evitar comentários óbvios linha a linha.
- **Segurança obrigatória**: usar **sempre** instruções SQL parametrizadas (`?`) em Python/Flask. Nunca concatenar input do utilizador em strings SQL.
- **Funcionamento 100% offline**: a app Flask não deve depender de CDNs externos (nem fontes, nem CSS/JS da internet).

---

## 2. Onde Colocar Cada Ficheiro

```text
billionaires_db_project/
├── AGENTS.md                 # Estas regras (para humanos e agentes de IA)
├── README.md                 # Guia geral do projeto e como correr a app
├── requirements.txt          # Dependências Python (Flask, pandas, etc.)
├── .gitignore                # Ignora venv/, __pycache__/, .DS_Store
│
├── server.py                 # Arranque do servidor Flask (porta 9000)         [P4]
├── app.py                    # Rotas Flask (/, /T, /T/k, /queries/1..10)      [P4]
├── db.py                     # Ligação SQLite (aponta para billionaires.db)   [P4]
├── test_db_connection.py     # Teste rápido de ligação a uma tabela           [P4]
├── billionaires.db           # Base de dados SQLite FINAL (na raiz!)          [P2]
├── templates/                # Templates Jinja HTML                           [P4]
├── static/                   # CSS e imagens estáticas                        [P4]
│
├── sql/
│   ├── schema.sql            # DDL final em SQLite (3FN, PKs, FKs, CHECK)     [P2]
│   └── queries.sql           # As 10 interrogações SQL testadas               [P3]
│
├── scripts/
│   └── populate.py           # Script reprodutível de limpeza e povoamento    [P2]
│
├── data/
│   └── ...                   # Dataset CSV/Excel original ou limpo            [P2]
│
└── docs/
    ├── er_diagram.png        # Diagrama ER em alta resolução (draw.io / Dia)  [P1]
    ├── relational_diagram.png# Diagrama Relacional 3FN com PKs e FKs          [P1]
    ├── seccao1_modelacao.md  # Texto da Secção 1 (ou .docx)                   [P1]
    ├── seccao2_bd.md         # Texto da Secção 2.1 (povoamento e contagens)   [P2]
    ├── seccao2_queries.md    # Texto da Secção 2.2 (10 queries + resultados)  [P3]
    ├── relatorio.docx        # Relatório final consolidado                    [P4]
    └── slides/               # Apresentação final                             [P4]
```

> **Nota importante do enunciado:** o ficheiro `billionaires.db` **tem de ficar na raiz** (na mesma pasta que `app.py` e `db.py`).
> Os ficheiros `create_mock_db.py` e `billionaires_mock.db` são temporários para desenvolvimento da app e devem ser removidos antes da entrega final no Moodle.

---

## 3. Regras de Integração por Pessoa

### Pessoa 1 — Modelação (ER + Relacional 3FN)
- Colocar diagramas em `docs/` exportados em **PNG de alta resolução** (ou SVG) e, se possível, também o ficheiro fonte (`.drawio` / `.dia`).
- Usar nomes de tabelas e colunas em `snake_case`, sem acentos nem espaços (ex.: `billionaires`, `country_id`, `net_worth_million`), alinhados com a Pessoa 2.
- Confirmar explicitamente PKs, FKs e justificação de 3FN.

### Pessoa 2 — Base de Dados SQLite (DDL + Povoamento)
- Colocar o DDL em `sql/schema.sql` com `PRAGMA foreign_keys = ON`, PKs, FKs, `NOT NULL`, `UNIQUE` e `CHECK` adequados.
- Colocar o script de limpeza/povoamento em `scripts/populate.py`, gerando `billionaires.db` na raiz do repositório.
- Validar sempre antes de fazer commit:
  - `PRAGMA foreign_key_check;` sem erros;
  - contagem de registos por tabela (para a tabela da Secção 2.1 do relatório).
- Avisar o grupo (sobretudo P3 e P4) sempre que alterar nomes de tabelas ou colunas.

### Pessoa 3 — 10 Interrogações SQL
- Colocar todas as 10 queries em `sql/queries.sql`, numeradas de `Q1` a `Q10`, com título e descrição em comentário acima de cada query:
  ```sql
  -- Q1: Título claro da interrogação
  -- Descrição: O que a interrogação calcula e porquê.
  SELECT ...
  ```
- **Para facilitar os links HTML na app Flask (P4):** sempre que uma query devolver registos de uma entidade (ex.: bilionário, país, indústria), incluir também a respetiva chave primária (`id`) no `SELECT` para a app conseguir criar links clicáveis (`/T/k`).
- Testar todas as 10 queries diretamente sobre `billionaires.db` antes de fazer push.

### Pessoa 4 — App Flask + Relatório Final + Entrega
- Manter `app.py`, `db.py`, `server.py`, `templates/` e `static/` na raiz, compatíveis com o `app.zip` da UC (porta `9000`).
- Garantir os requisitos do enunciado:
  - `/` (página de entrada com acesso a todas as tabelas e às 10 interrogações);
  - `/T` e `/T/k` para cada tabela de entidade;
  - 1 endpoint por cada uma das 10 interrogações;
  - links HTML (`<a href=...>`) por chaves estrangeiras em todas as páginas;
  - SQL parametrizado (`?`) em todas as queries com parâmetros.
- Antes da submissão no Moodle (11 de dezembro): remover `billionaires_mock.db` e `create_mock_db.py`, testar tudo com `billionaires.db` final e rever o `docs/relatorio.docx`.

---

## 4. Boas Práticas de Git no Grupo

- Fazer sempre `git pull` antes de começar a trabalhar.
- Não fazer commit de `venv/`, `__pycache__/`, `.DS_Store` nem ficheiros temporários.
- Fazer commits pequenos e claros (ex.: `Add SQLite schema and populate script`, `Add SQL queries Q1-Q10`).
- Não alterar ficheiros de outra pessoa sem combinar antes com o grupo.
