# ADR-0008: REST/JSON como estilo de API

## Status

Aceito

## Date

2026-06-29

## Context

A aplicação é consumida por uma **Aplicação Web** externa (e potencialmente outros
clientes). É preciso definir o **estilo de interface**: protocolo, formato de
dados e contrato. O requisito é interoperabilidade ampla, baixa fricção de
integração e contrato bem documentado.

## Decision

Expor uma **API REST sobre HTTP** com payloads em **JSON**, recursos orientados a
substantivos (`/reclamacoes`, `/sugestoes`), verbos HTTP semânticos e códigos de
status apropriados (`201`, `202`, `200`, `4xx`, `5xx`). O contrato é documentado
automaticamente via **OpenAPI/Swagger** (nativo do FastAPI).

## Alternatives Considered

### Alternative 1: GraphQL

- **Description**: Endpoint único com consultas flexíveis.
- **Pros**: Cliente busca exatamente o que precisa; evita _over/under-fetching_.
- **Cons**: Complexidade de servidor, cache e segurança; _overkill_ para o domínio.
- **Why rejected**: Domínio com recursos bem definidos não justifica a complexidade.

### Alternative 2: gRPC

- **Description**: RPC binário sobre HTTP/2 com contratos `.proto`.
- **Pros**: Alto desempenho, contrato forte, _streaming_.
- **Cons**: Menor interoperabilidade com navegadores; tooling extra.
- **Why rejected**: Consumidor principal é web; REST/JSON tem menor fricção.

## Consequences

### Positive

- Interoperabilidade ampla; fácil de consumir e testar (curl, navegador, Postman).
- Documentação OpenAPI automática.
- Ecossistema maduro (auth, cache HTTP, gateways).

### Negative

- _Over/under-fetching_ ocasional comparado ao GraphQL.
- Versionamento de contrato precisa de disciplina.

### Risks

- Mudanças que quebram o contrato → mitigado com versionamento (`/v1`) e testes de contrato.

## Implementation Notes

- Prefixo de versão `/v1`.
- Operações longas retornam `202 Accepted` + recurso de status (ver [ADR-0007](0007-processamento-assincrono-de-ia.md)).
- Erros em formato padronizado (ex.: Problem Details, RFC 9457).

## References

- [arquitetura.md — Seção 5 (Containers)](../arquitetura.md)
