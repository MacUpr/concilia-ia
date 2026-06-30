# ADR-0001: Aplicação como única API REST (mono-serviço)

## Status

Aceito

## Date

2026-06-29

## Context

A aplicação a ser desenvolvida pelo grupo é o serviço de back-end que concentra
**todo o processamento de IA** da Conciliação (classificação de reclamações e
geração de sugestões). A interface de usuário (Aplicação Web), o Sistema TJMS e os
provedores de LLM são externos e fora do escopo de desenvolvimento.

A primeira modelagem do projeto sugeria um sistema distribuído com vários serviços
(Backend, Serviço de Conciliação, Serviço de IA), mas isso introduz complexidade
operacional (rede, _deploy_, observabilidade distribuída) sem benefício claro para
o tamanho atual da equipe e do problema.

## Decision

A aplicação será **uma única API REST** (um único serviço _deployável_), que
expõe os endpoints e concentra as regras de negócio e o processamento de IA.
A separação interna se dá por **componentes/módulos** (camada de endpoints,
serviços de domínio, gateway de LLM, repositórios), não por serviços de rede
independentes. Um **Worker** assíncrono complementar compartilha o mesmo código
(ver [ADR-0007](0007-processamento-assincrono-de-ia.md)).

## Alternatives Considered

### Alternative 1: Arquitetura de microsserviços

- **Description**: Separar Conciliação, Classificação e IA em serviços distintos.
- **Pros**: Escala/_deploy_ independente por serviço; isolamento de falhas.
- **Cons**: _Overhead_ de rede, _deploy_ e observabilidade; complexidade alta para o time.
- **Why rejected**: Custo desproporcional ao tamanho atual do problema e da equipe.

### Alternative 2: Aplicação monolítica com interface acoplada (server-side rendering)

- **Description**: Back-end e front-end no mesmo monólito.
- **Pros**: Tudo num lugar só.
- **Cons**: Acopla a UI ao back-end; o escopo é explicitamente só a API.
- **Why rejected**: O front-end é externo e consumido por múltiplos clientes.

## Consequences

### Positive

- Operação e _deploy_ simples; menor superfície de falha.
- Refatoração interna barata (chamadas em processo, não em rede).
- Fronteiras claras via componentes — caminho aberto para extrair serviços depois.

### Negative

- Acoplamento interno maior que microsserviços.
- Escala é do serviço inteiro (mitigado em parte pelo Worker independente).

### Risks

- Crescimento futuro pode exigir extração de serviços → mitigado mantendo
  módulos coesos e com fronteiras bem definidas (ports/adapters).

## Implementation Notes

Organizar o código em camadas (`api/`, `services/`, `domain/`, `adapters/`,
`repositories/`) para permitir extração futura de um módulo em serviço próprio
com baixo custo.

## References

- [arquitetura.md — Seção 2 (Escopo)](../arquitetura.md)
- [ADR-0007 — Processamento assíncrono de IA](0007-processamento-assincrono-de-ia.md)
