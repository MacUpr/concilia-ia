# ADR-0010: Observabilidade (logs, métricas, tracing)

## Status

Proposto

## Date

2026-06-29

## Context

O sistema integra dependências externas instáveis (LLMs, TJMS) e processa trabalho
de forma assíncrona (fila + worker). Sem observabilidade, é difícil diagnosticar
latência, falhas de provedor, acúmulo de fila e qualidade das sugestões. Por ser
um domínio sensível, também é necessário medir **uso de IA** e **comportamento da
validação humana**.

## Decision

Adotar os três pilares de observabilidade:

1. **Logs estruturados** (JSON) com correlação por `request_id`/`task_id`, **sem**
   dados sensíveis em texto puro.
2. **Métricas** (ex.: Prometheus): latência por endpoint, taxa de erro, tempo e
   custo das chamadas de LLM, profundidade da fila, tempo até validação humana.
3. **_Tracing_ distribuído** (OpenTelemetry) cobrindo o caminho API → fila → Worker
   → LLM.

## Alternatives Considered

### Alternative 1: Apenas logs simples (texto não estruturado)

- **Description**: `print`/log básico em texto.
- **Pros**: Trivial de começar.
- **Cons**: Difícil de consultar/correlacionar; sem métricas nem _tracing_.
- **Why rejected**: Insuficiente para depurar fluxo assíncrono e dependências externas.

### Alternative 2: APM proprietário completo (ex.: Datadog) desde já

- **Description**: Plataforma paga de observabilidade ponta a ponta.
- **Pros**: Recursos ricos, pouca configuração.
- **Cons**: Custo; possível _lock-in_.
- **Why rejected**: Padrões abertos (OpenTelemetry/Prometheus) evitam _lock-in_; APM pode entrar depois.

## Consequences

### Positive

- Diagnóstico rápido de latência, erros e gargalos da fila.
- Métricas de **qualidade da IA** e de validação humana para decisões de evolução.
- Padrões abertos → portabilidade de _backend_ de observabilidade.

### Negative

- Esforço de instrumentação e operação dos coletores.
- Cuidado para **não** registrar dados sensíveis ([ADR-0009](0009-protecao-de-dados-de-saude-e-lgpd.md)).

### Risks

- _Overhead_/custo de telemetria → mitigado com amostragem de _traces_ e retenção adequada.

## Implementation Notes

- Logging estruturado com `request_id` propagado até o Worker.
- Exportadores OpenTelemetry; métricas no formato Prometheus.
- _Dashboards_ e alertas para taxa de erro de LLM e profundidade de fila.

## References

- [ADR-0007 — Processamento assíncrono de IA](0007-processamento-assincrono-de-ia.md)
- [arquitetura.md — Seção 10 (RNFs) e Seção 14 (Evolução)](../arquitetura.md)
