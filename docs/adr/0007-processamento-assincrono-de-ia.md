# ADR-0007: Processamento assíncrono de IA (fila + worker)

## Status

Aceito

## Date

2026-06-29

## Context

As análises de IA (classificação + geração de sugestão) dependem de LLMs externos,
cujas respostas podem levar de **segundos a dezenas de segundos** e estão sujeitas
a latência variável e indisponibilidade. Executar isso **dentro** do ciclo
requisição/resposta HTTP prejudica a experiência (timeouts, conexões presas) e a
resiliência da API.

## Decision

Processar a IA de forma **assíncrona**: a API REST **persiste a reclamação,
enfileira** a tarefa de análise (Redis) e responde imediatamente (`202 Accepted` /
recurso com status `PENDENTE`). Um **Worker** (Celery) consome a fila, chama o LLM
via Gateway, persiste a sugestão e atualiza o status. O cliente acompanha por
_polling_ (`GET /sugestoes/{id}`) ou _webhook_/_callback_.

## Alternatives Considered

### Alternative 1: Processamento síncrono (chamar o LLM dentro do request)

- **Description**: A requisição HTTP espera a resposta do LLM.
- **Pros**: Simples; sem fila nem worker.
- **Cons**: _Timeouts_, conexões longas, baixa resiliência a latência/falha do LLM.
- **Why rejected**: Inadequado para chamadas externas lentas e instáveis.

### Alternative 2: Streaming síncrono (Server-Sent Events)

- **Description**: Manter a conexão aberta transmitindo a resposta do LLM.
- **Pros**: Boa UX para geração de texto em tempo real.
- **Cons**: Conexões longas, escala mais difícil, acopla UI ao tempo do LLM.
- **Why rejected**: Útil no futuro para UX, mas não resolve resiliência/escala do back-end.

## Consequences

### Positive

- API responsiva e resiliente à latência/falha do LLM.
- Worker escala independentemente conforme a profundidade da fila.
- _Retry_/_backoff_ e _fallback_ de provedor tratados fora do request.

### Negative

- Complexidade adicional (fila, worker, estados, _eventual consistency_).
- Cliente precisa lidar com resultado **assíncrono** (polling/callback).

### Risks

- Tarefas duplicadas/parciais → mitigado com **idempotência** e estados explícitos.
- Acúmulo de fila em pico → mitigado com _autoscaling_ do Worker e _backpressure_.

## Implementation Notes

- `POST /reclamacoes` → persiste + enfileira → `202` com `id` e `status=PENDENTE`.
- Worker idempotente; _retry_ com _backoff_ exponencial; _dead-letter_ para falhas persistentes.
- Estados: `PENDENTE → PROCESSANDO → SUGERIDA → (validação humana)`.

## References

- [ADR-0006 — Redis para cache e fila](0006-redis-cache-e-fila.md)
- [arquitetura.md — Seção 5 (Containers)](../arquitetura.md)
