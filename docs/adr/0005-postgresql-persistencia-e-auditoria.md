# ADR-0005: PostgreSQL para persistência e auditoria

## Status

Aceito

## Date

2026-06-29

## Context

O sistema precisa persistir reclamações, sugestões, decisões validadas e uma
**trilha de auditoria**. Os dados são majoritariamente **relacionais e
transacionais** (entidades com relacionamentos, estados e integridade
referencial), com requisito forte de **consistência** e **rastreabilidade**.
Pode haver também conteúdo semiestruturado (payloads de IA, metadados).

## Decision

Usar **PostgreSQL** como banco de dados relacional principal, com transações ACID
para garantir consistência das decisões e da auditoria. Campos semiestruturados
(ex.: resposta bruta do LLM, metadados) usam colunas **`JSONB`**.

## Alternatives Considered

### Alternative 1: Banco NoSQL de documentos (ex.: MongoDB)

- **Description**: Persistir tudo como documentos.
- **Pros**: Flexível para dados semiestruturados.
- **Cons**: Transações/relacionamentos e integridade referencial mais fracos.
- **Why rejected**: O modelo é relacional e exige consistência forte para auditoria.

### Alternative 2: SQLite

- **Description**: Banco embarcado em arquivo.
- **Pros**: Zero operação; ótimo para desenvolvimento.
- **Cons**: Concorrência/escala limitadas para produção.
- **Why rejected**: Inadequado para acesso concorrente em produção (útil só em testes).

## Consequences

### Positive

- ACID garante consistência de decisões e auditoria.
- `JSONB` cobre necessidades semiestruturadas sem outro banco.
- Ferramentas maduras (migrações, _backup_, réplicas).

### Negative

- Requer operação de banco (gerenciado mitiga isso).
- Esquema relacional exige migrações disciplinadas.

### Risks

- Crescimento da trilha de auditoria → mitigado com particionamento/retenção e
  índices adequados.

## Implementation Notes

- ORM/Repositórios com SQLAlchemy; migrações com Alembic.
- Tabela de auditoria **append-only** (sem update/delete) para integridade.
- Criptografia de dados sensíveis em repouso ([ADR-0009](0009-protecao-de-dados-de-saude-e-lgpd.md)).

## References

- [arquitetura.md — Seção 5 (Containers)](../arquitetura.md)
