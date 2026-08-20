# ADR-0006: Alembic para versionamento e migração de schema

## Status

Aceito

## Data

2026-07-14

## Contexto

O banco **PostgreSQL** ([ADR-0005](0005-postgresql-sqlalchemy.md)) evolui ao longo
das _sprints_ (cadastros, solicitações, análises, auditoria e embeddings do
pgvector). É preciso **versionar** as mudanças de schema de forma **controlada,
reproduzível e reversível**, aplicadas de maneira idêntica em vários ambientes
(dev/prod), evitando alterações manuais e _drift_. O sistema já usa SQLAlchemy.

## Decisão

Usar **Alembic** (companheiro do SQLAlchemy) para **migrações versionadas** de
schema. Cada mudança é uma **revisão** no repositório (com `upgrade` e
`downgrade`), aplicada de forma **determinística**. As migrações fazem parte do
**processo de _deploy_**.

## Alternativas Consideradas

### Alternativa 1: SQL manual / scripts ad-hoc

- **Descrição**: Escrever e aplicar SQL de alteração à mão.
- **Prós**: Controle total sobre o SQL.
- **Contras**: Sem histórico versionado; propenso a _drift_ e erro humano.
- **Por que rejeitada**: Não rastreável nem reproduzível entre ambientes.

### Alternativa 2: Auto-create do ORM (`create_all`)

- **Descrição**: Deixar o SQLAlchemy criar as tabelas a partir dos modelos.
- **Prós**: Rápido no início do desenvolvimento.
- **Contras**: Não gerencia alterações incrementais nem produção.
- **Por que rejeitada**: Inadequado para produção e para a auditabilidade exigida.

## Consequências

### Positivas

- Histórico de schema **versionado no Git**; revisável em _pull request_.
- Reprodutível entre ambientes; integra-se ao SQLAlchemy.

### Negativas

- Exige disciplina para escrever e revisar migrações.
- Migrações de **dados** exigem cuidado extra.

### Riscos

- Migração destrutiva em produção → **revisão obrigatória**, **backup** antes e
  migrações **reversíveis** quando possível.

## Notas de Implementação

- `alembic revision --autogenerate`, sempre **revisado manualmente**.
- A migração inicial cria a **extensão `vector`** de forma idempotente.
- Migrações executadas no _pipeline_ **antes** de subir a aplicação ([ADR-0011](0011-docker.md)).

## Referências

- [arquitetura-c4.md — Seção 5](../arquitetura-c4.md)
- [ADR-0005 — PostgreSQL + SQLAlchemy](0005-postgresql-sqlalchemy.md)
