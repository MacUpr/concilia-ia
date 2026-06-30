# ADR-0006: Redis para cache e fila

## Status

Aceito

## Date

2026-06-29

## Context

Chamadas a LLMs são **lentas e caras**. Reclamações semelhantes podem gerar
consultas repetidas, e respostas idempotentes podem ser reaproveitadas. Além
disso, o processamento de IA precisa ser **assíncrono**
([ADR-0007](0007-processamento-assincrono-de-ia.md)), o que exige um _broker_ de
mensagens entre a API REST e o Worker.

## Decision

Usar **Redis** para dois papéis:

1. **Cache** de respostas de LLM idempotentes e de consultas frequentes, reduzindo
   latência e custo.
2. **Fila / _broker_** das tarefas assíncronas de IA (backend do Celery).

## Alternatives Considered

### Alternative 1: Sem cache; fila dedicada (RabbitMQ/Kafka)

- **Description**: _Broker_ dedicado para mensageria e nenhum cache.
- **Pros**: _Broker_ robusto e recursos avançados de mensageria.
- **Cons**: Mais um componente para operar; sem ganho de cache; complexidade desnecessária na fase atual.
- **Why rejected**: Redis cobre cache **e** fila com um único componente simples.

### Alternative 2: Cache em memória do processo (in-process)

- **Description**: Cache local na instância da API.
- **Pros**: Mais simples, sem dependência externa.
- **Cons**: Não compartilhado entre réplicas; perde-se no _restart_.
- **Why rejected**: API é replicável e _stateless_; cache precisa ser compartilhado.

## Consequences

### Positive

- Um só componente para cache e fila → menos operação.
- Reduz latência e custo de chamadas repetidas ao LLM.
- Desacopla API REST e Worker.

### Negative

- Dado em cache pode ficar **obsoleto** (_staleness_) → exige TTL e chaves bem definidas.
- Redis vira dependência crítica da fila (mitigado por serviço gerenciado/HA).

### Risks

- Garantias de entrega mais fracas que um _broker_ dedicado → mitigado com tarefas
  **idempotentes** e _retry_; reavaliar broker dedicado se o volume crescer.

## Implementation Notes

- Cache: chave por _hash_ do prompt/entrada normalizada + TTL.
- Fila: Celery com _broker_ Redis; tarefas idempotentes e com _retry_ exponencial.

## References

- [ADR-0007 — Processamento assíncrono de IA](0007-processamento-assincrono-de-ia.md)
- [ADR-0003 — Abstração multiprovedor de LLM](0003-abstracao-multiprovedor-llm.md)
