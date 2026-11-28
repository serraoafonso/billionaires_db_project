# Billionaires Statistics · Projeto de Bases de Dados

Projeto da unidade curricular **Bases de Dados (CC2005)** da Faculdade de Ciências da Universidade do Porto (FCUP). O objetivo é modelar e construir uma base de dados relacional em SQLite a partir do **Billionaires Statistics Dataset** e disponibilizá-la numa aplicação web em Python com Flask.

> **Regras para o grupo e agentes de IA:** ver [AGENTS.md](AGENTS.md) antes de adicionar ou alterar código.
> **Princípio base:** manter todo o código (Python, SQL, HTML e CSS) **o mais simples e percetível possível para um humano**, sem abstrações desnecessárias, fácil de ler e explicar na apresentação oral.

---

## Estrutura do repositório (onde colocar cada ficheiro)

| Caminho | Responsável | Conteúdo |
| --- | --- | --- |
| `docs/` | **Pessoa 1** | Diagramas ER e Relacional (3FN) em PNG/SVG + texto da Secção 1 |
| `sql/schema.sql` | **Pessoa 2** | Script DDL SQLite (PKs, FKs, tipos, `NOT NULL`, `UNIQUE`, `CHECK`) |
| `scripts/populate.py` | **Pessoa 2** | Script Python/Pandas reprodutível de limpeza e povoamento |
| `data/` | **Pessoa 2** | Dataset original / ficheiros CSV auxiliares |
| `billionaires.db` *(na raiz)* | **Pessoa 2** | Base de dados SQLite final (tem de ficar na mesma pasta que `app.py`) |
| `sql/queries.sql` | **Pessoa 3** | As 10 interrogações SQL testadas + comentários com título e descrição |
| `app.py`, `db.py`, `server.py`, `templates/`, `static/` | **Pessoa 4** | Aplicação web Flask (`/`, `/T`, `/T/k`, 10 queries, links por FK, SQL `?`) |
| `docs/relatorio.docx` e `docs/slides/` | **Pessoa 4** | Relatório final consolidado e slides da apresentação |

*Nota: `create_mock_db.py` e `billionaires_mock.db` são apenas temporários para testar a app Flask enquanto a base de dados final não é entregue.*

---

## Como executar a aplicação Flask localmente

1. Criar e ativar o ambiente virtual e instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

2. *(Opcional, em modo mock)* Recriar a base de dados temporária de testes:

```bash
python3 create_mock_db.py
```

3. Testar a ligação à base de dados (exemplo com a tabela `countries`):

```bash
python3 test_db_connection.py countries
```

4. Iniciar o servidor Flask:

```bash
python3 server.py
```

Abrir no browser: **http://127.0.0.1:9000**

---

## Rotas da aplicação web

Nas rotas abaixo, `T` corresponde a uma tabela de entidade e `k` à chave primária de um registo.

| Rota | Funcionalidade |
| --- | --- |
| `/` | Página inicial com acesso a todas as tabelas e às 10 interrogações. |
| `/T` | Lista de registos da tabela `T`, com links para `/T/k` e entidades relacionadas. |
| `/T/k` | Detalhe do registo `k` da tabela `T`, com links HTML por chaves estrangeiras. |
| `/queries/1` … `/queries/10` | Execução de cada uma das 10 interrogações SQL, com resultados e links HTML. |

Todas as interrogações com parâmetros utilizam **instruções SQL parametrizadas (`?`)** para prevenir injeção de SQL.

---

## Entrega

- **Prazo no Moodle:** 11 de dezembro (relatório, base de dados `billionaires.db` e aplicação Flask).
- **Apresentação:** semana de 14 a 18 de dezembro.
- Antes da entrega final, remover os ficheiros temporários de mock (`create_mock_db.py` e `billionaires_mock.db`) e confirmar `DB_FILE = 'billionaires.db'` em `db.py`.
