# C4 — Dinâmico: Fluxo do pedido à conciliação

Sequência numerada do fluxo principal: do registro do pedido até a validação
humana da sugestão. Público: técnico.

> Notação: **diagrama de sequência** (visão dinâmica do C4), com passos numerados
> automaticamente.

```mermaid
---
config:
  theme: base
  themeVariables:
    fontFamily: "Segoe UI, Helvetica, Arial, sans-serif"
    primaryColor: "#eef4fb"
    primaryBorderColor: "#0b4884"
    primaryTextColor: "#10263b"
    lineColor: "#61728a"
    actorBkg: "#1168bd"
    actorTextColor: "#ffffff"
    actorBorder: "#0b4884"
    signalColor: "#33415c"
    signalTextColor: "#10263b"
    noteBkgColor: "#fff3d6"
    noteBorderColor: "#e0b64a"
    labelBoxBkgColor: "#eef4fb"
    labelBoxBorderColor: "#0b4884"
  sequence:
    useMaxWidth: true
    diagramMarginX: 20
    messageFontSize: 13
    actorFontSize: 13
    noteFontSize: 12
---
sequenceDiagram
  autonumber
  actor Servidor as Servidor do CEJUSC
  participant Web as Aplicação Web
  participant API as API REST
  participant ST as Object Storage
  participant DB as PostgreSQL + pgvector
  participant LLM as Provedor de LLM
  actor Conciliador

  Servidor->>Web: Registra pedido e anexa documentos
  Web->>API: POST /solicitacoes e /upload
  API->>ST: Armazena os arquivos
  Web->>API: POST /analise
  API->>DB: Busca por similaridade das normas e cláusulas
  API->>LLM: Solicita sugestão com o contexto recuperado
  LLM-->>API: Sugestão fundamentada
  API->>DB: Persiste sugestão PENDENTE e auditoria
  API-->>Web: Retorna o resultado PENDENTE
  Conciliador->>Web: Revisa e valida a sugestão
  Web->>API: Registra a decisão
  API->>DB: Atualiza o status e audita
```

## Notas

- A sugestão nasce **`PENDENTE`** (passo 8) e só vira decisão após a **validação
  humana** (passos 10–12) — ver [ADR-0009](../adr/0009-validacao-humana.md).
- O contexto recuperado (passos 5–6) fundamenta a sugestão e é registrado na
  auditoria — ver [ADR-0007](../adr/0007-pgvector-rag.md) e
  [ADR-0012](../adr/0012-explicabilidade-auditoria.md).
