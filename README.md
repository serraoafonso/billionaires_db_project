# Billionaires Statistics · Projeto de Bases de Dados

Projeto da unidade curricular **Bases de Dados (CC2005)** da Faculdade de Ciências da Universidade do Porto (FCUP). O objetivo é transformar os dados do **Billionaires Statistics Dataset** numa base de dados relacional em SQLite e disponibilizá-los numa aplicação web em Python com Flask.

**Estado do projeto.** O repositório contém atualmente a documentação inicial.

## Modelação e base de dados

1. Descrever os requisitos do domínio e representá-los num diagrama Entidade–Relacionamento (ER).
2. Converter o modelo ER num esquema relacional em **3.ª forma normal (3FN)**, identificando as chaves primárias e estrangeiras.
3. Criar as tabelas em SQLite com tipos de dados e restrições adequados e preenchê-las com os dados do conjunto atribuído.
4. Elaborar **10 consultas SQL** de complexidade variável que extraiam informação relevante do conjunto de dados e apliquem as técnicas estudadas na unidade curricular.

A modelação deverá ser validada com o docente nas aulas práticas antes da implementação.

## Aplicação web

A aplicação Flask deverá seguir a estrutura do `app.zip` disponibilizado na unidade curricular. Nas rotas abaixo, `T` corresponde a uma tabela que representa uma entidade e `k` à chave primária de um registo.

| Rota | Funcionalidade |
| --- | --- |
| `/` | Página inicial com acesso às listas de registos e às consultas SQL. |
| `/T` | Lista de registos da tabela `T`, com ligações para as respetivas páginas de detalhe. |
| `/T/k` | Detalhe do registo `k` da tabela `T`. |

A aplicação terá também uma rota para cada uma das **10 consultas SQL**. As páginas deverão incluir ligações HTML para os dados relacionados por chaves estrangeiras, e o código deverá usar instruções SQL parametrizadas para prevenir a injeção de SQL.

## Entrega

A entrega é feita via Moodle e inclui o relatório, a base de dados SQLite preenchida e a aplicação Flask. O relatório deverá seguir o modelo disponibilizado na unidade curricular e explicar o mapeamento entre o modelo ER e o esquema relacional.
