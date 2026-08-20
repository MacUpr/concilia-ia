# ADR-0003: REST/JSON com documentação OpenAPI (Swagger)

## Status

Aceito

## Data

2026-07-14

## Contexto

A solução é consumida por uma **Aplicação Web** (telas de login, dashboard, nova
solicitação, upload, resultado) e, potencialmente, por outros clientes. É preciso
definir o **estilo de interface**: protocolo, formato de dados e forma de
documentar o contrato. O PDF já indica os endpoints (`POST /login`,
`POST /solicitacoes`, `GET /solicitacoes`, `POST /upload`, `POST /analise`,
`GET /resultado`) e o uso de **Swagger**.

## Decisão

Expor uma **API REST sobre HTTP** com payloads em **JSON**, recursos orientados a
substantivos, verbos HTTP semânticos e códigos de status apropriados. O contrato é
documentado automaticamente via **OpenAPI/Swagger** (nativo do FastAPI).

## Alternativas Consideradas

### Alternativa 1: GraphQL

- **Descrição**: Endpoint único com consultas flexíveis.
- **Prós**: Cliente busca exatamente o que precisa.
- **Contras**: Complexidade de servidor, cache e segurança; _overkill_ para o MVP.
- **Por que rejeitada**: Recursos bem definidos não justificam a complexidade.

### Alternativa 2: gRPC

- **Descrição**: RPC binário sobre HTTP/2.
- **Prós**: Alto desempenho e contrato forte.
- **Contras**: Menor interoperabilidade com navegadores; ferramental extra.
- **Por que rejeitada**: O consumidor principal é web; REST/JSON tem menos fricção.

## Consequências

### Positivas

- Interoperabilidade ampla; fácil de testar (curl, navegador, Postman).
- Documentação **Swagger** automática e sempre atualizada.
- Ecossistema maduro (auth, cache HTTP, gateways).

### Negativas

- _Over/under-fetching_ ocasional comparado ao GraphQL.
- Versionamento de contrato exige disciplina.

### Riscos

- Mudanças que quebram o contrato → mitigadas por versionamento (`/v1`) e testes.

## Notas de Implementação

- Prefixo de versão `/v1`.
- Erros em formato padronizado (ex.: Problem Details, RFC 9457).
- Autenticação via _bearer token_ JWT ([ADR-0004](0004-autenticacao-jwt.md)).

## Referências

- [arquitetura-c4.md — Seção 5](../arquitetura-c4.md)
- [ADR-0002 — Python + FastAPI](0002-python-fastapi.md)
