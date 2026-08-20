# ADR-0005: PostgreSQL + SQLAlchemy para persistência

## Status

Aceito

## Data

2026-07-14

## Contexto

O sistema precisa persistir **usuários, planos, operadoras, contratos,
solicitações, análises e uma trilha de auditoria**. Os dados são majoritariamente
**relacionais e transacionais** (entidades com relacionamentos, estados e
integridade referencial), com forte requisito de **consistência** e
**rastreabilidade**. Também há conteúdo semiestruturado (respostas da IA,
metadados) e necessidade futura de **busca vetorial** (ver [ADR-0007](0007-pgvector-rag.md)).

## Decisão

Usar **PostgreSQL** como banco relacional principal, com transações ACID, acessado
via **SQLAlchemy** (ORM/repositórios). Campos semiestruturados usam colunas
**`JSONB`**. O mesmo PostgreSQL hospeda os embeddings vetoriais (pgvector),
evitando um segundo banco.

## Alternativas Consideradas

### Alternativa 1: Banco NoSQL de documentos (ex.: MongoDB)

- **Descrição**: Persistir tudo como documentos.
- **Prós**: Flexível para dados semiestruturados.
- **Contras**: Transações/relacionamentos e integridade referencial mais fracos.
- **Por que rejeitada**: O modelo é relacional e exige consistência forte para auditoria.

### Alternativa 2: SQLite

- **Descrição**: Banco embarcado em arquivo.
- **Prós**: Zero operação; ótimo para desenvolvimento.
- **Contras**: Concorrência e escala limitadas.
- **Por que rejeitada**: Inadequado para produção concorrente (útil só em testes).

## Consequências

### Positivas

- ACID garante consistência das decisões e da auditoria.
- `JSONB` cobre o semiestruturado; **pgvector** cobre a busca semântica — tudo em
  um só banco.
- Ferramental maduro (migrações, _backup_, réplicas).

### Negativas

- Requer operação de banco (serviço gerenciado mitiga).
- Esquema relacional exige migrações disciplinadas.

### Riscos

- Crescimento da trilha de auditoria → mitigado por índices, particionamento e
  política de retenção.

## Notas de Implementação

- ORM/Repositórios com SQLAlchemy; migrações com **Alembic** ([ADR-0006](0006-alembic-migracoes.md)).
- Tabela de auditoria **append-only** (sem update/delete).
- Extensão `vector` habilitada no banco ([ADR-0007](0007-pgvector-rag.md)).

## Referências

- [arquitetura-c4.md — Seção 5](../arquitetura-c4.md)
- [ADR-0006 — Alembic para migrações](0006-alembic-migracoes.md)
- [ADR-0007 — pgvector para RAG](0007-pgvector-rag.md)
