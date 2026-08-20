# ADR-0009: Validação humana obrigatória (human-in-the-loop)

## Status

Aceito

## Data

2026-07-14

## Contexto

A jornada do usuário prevê: **IA analisa → sistema gera sugestão → conciliador
valida → finaliza a conciliação**. A IA é **probabilística** e pode **errar ou
alucinar**; a decisão trata de **direitos em saúde** e tem impacto jurídico. Uma
das hipóteses do projeto é que **o conciliador confiará nas recomendações da IA** —
o que só é aceitável com **controle humano** e uso de **IA responsável**.

## Decisão

A sugestão da IA **nunca** é aplicada automaticamente. Toda sugestão nasce no
estado **`PENDENTE`** e só se torna decisão após **validação humana** do
conciliador (aprovar, ajustar ou rejeitar). O sistema apoia, mas **não substitui**
a decisão humana.

## Alternativas Consideradas

### Alternativa 1: Decisão automática da IA

- **Descrição**: Aplicar a sugestão sem revisão humana.
- **Prós**: Máxima velocidade e automação.
- **Contras**: Risco jurídico e ético; erros/alucinação sem barreira.
- **Por que rejeitada**: Inaceitável para decisões sobre saúde.

### Alternativa 2: Automação parcial por limiar de confiança

- **Descrição**: Auto-aprovar casos simples acima de um _score_.
- **Prós**: Ganho de eficiência em casos triviais.
- **Contras**: Difícil calibrar; risco residual sem histórico validado.
- **Por que rejeitada agora**: Prematuro no MVP; fica como **evolução** com revisão
  por amostragem.

## Consequências

### Positivas

- Segurança jurídica e **confiança** do conciliador na ferramenta.
- Gera dados rotulados (sugestão vs. decisão) para avaliar a qualidade da IA.

### Negativas

- Mantém uma etapa manual (não é 100% automático).

### Riscos

- **Viés de automação** (aceitar sem revisar de fato) → mitigado apresentando a
  **fundamentação** e exigindo ação explícita ([ADR-0012](0012-explicabilidade-auditoria.md)).

## Notas de Implementação

- Estados da sugestão: `PENDENTE` → `APROVADA` / `AJUSTADA` / `REJEITADA`.
- Registrar **sugestão original da IA** e **ação do conciliador** (auditoria).
- Métrica de sucesso: taxa de sugestões aceitas (meta do PDF: > 80%).

## Referências

- [arquitetura-c4.md — Seção 7](../arquitetura-c4.md)
- [ADR-0008 — LLM multiprovedor](0008-llm-multiprovedor.md)
- [ADR-0012 — Explicabilidade e auditoria](0012-explicabilidade-auditoria.md)
