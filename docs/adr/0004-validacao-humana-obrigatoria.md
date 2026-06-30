# ADR-0004: Validação humana obrigatória (human-in-the-loop)

## Status

Aceito

## Date

2026-06-29

## Context

A IA gera **sugestões de conciliação** sobre demandas de saúde suplementar — um
domínio sensível, com impacto jurídico e na vida do beneficiário. Modelos de
linguagem são probabilísticos e podem **errar ou alucinar**. Aplicar
automaticamente uma sugestão da IA seria inaceitável do ponto de vista ético,
jurídico e de responsabilidade.

## Decision

Toda sugestão gerada pela IA entra com status **`PENDENTE`** e **só** produz efeito
após **validação explícita de um Conciliador CEJUSC**, que pode **aprovar, ajustar
ou rejeitar**. A IA nunca decide; ela **assiste** a decisão humana. A sugestão
original da IA e a ação do conciliador são registradas para auditoria
([ADR-0009](0009-protecao-de-dados-de-saude-e-lgpd.md)).

## Alternatives Considered

### Alternative 1: Automação total (a IA decide e aplica)

- **Description**: Aplicar a sugestão sem revisão.
- **Pros**: Máxima eficiência/throughput.
- **Cons**: Risco jurídico/ético inaceitável; sem responsabilização clara.
- **Why rejected**: Domínio sensível exige responsabilidade humana.

### Alternative 2: Automação com revisão por amostragem

- **Description**: Aplicar automaticamente e revisar só uma amostra.
- **Pros**: Equilíbrio entre eficiência e controle.
- **Cons**: Casos não amostrados aplicados sem revisão; ainda arriscado nesta fase.
- **Why rejected**: Prematuro; pode ser reavaliado após maturidade e métricas de qualidade.

## Consequences

### Positive

- Controle humano e responsabilização claros.
- Conformidade ética/jurídica; confiança institucional.
- Dados de revisão alimentam métricas de qualidade da IA.

### Negative

- _Throughput_ limitado pela capacidade humana de revisão.
- Latência até a decisão final (depende do conciliador).

### Risks

- Viés de automação (conciliador aprovar sem ler) → mitigado com UX que exige
  revisão consciente e registro de tempo/edições.

## Implementation Notes

- Máquina de estados da sugestão: `PENDENTE → APROVADA | AJUSTADA | REJEITADA`.
- Endpoint `POST /sugestoes/{id}/validar` exige identidade do conciliador.
- Persistir sugestão original + decisão + autor + timestamp.

## References

- [arquitetura.md — Seção 7 (Fluxo Dinâmico) e Seção 9 (Uso de IA)](../arquitetura.md)
