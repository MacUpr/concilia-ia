# C4 — Nível 1: Contexto (Concilia IA)

Mostra a **Concilia IA** como uma unidade e suas relações com pessoas e sistemas
externos. Público: todos os interessados.

> Notação: **flowchart** seguindo as convenções do C4 (melhor legibilidade que o
> `C4Context` nativo do Mermaid). Cores: azul-escuro = pessoa, azul = sistema em
> foco, cinza = sistema externo.

```mermaid
---
config:
  theme: base
  themeVariables:
    fontFamily: "Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: "14px"
    primaryColor: "#eef4fb"
    primaryBorderColor: "#0b4884"
    primaryTextColor: "#10263b"
    lineColor: "#61728a"
    clusterBkg: "#f6f9fc"
    clusterBorder: "#bccadd"
  flowchart:
    curve: basis
    htmlLabels: true
    padding: 16
    nodeSpacing: 55
    rankSpacing: 60
---
flowchart TB
  cidadao["<b>Cidadão / Beneficiário</b><br/><i>[Pessoa]</i><br/>Registra o pedido e<br/>acompanha o resultado"]
  servidor["<b>Servidor do CEJUSC</b><br/><i>[Pessoa]</i><br/>Registra e acompanha<br/>os pedidos"]
  conciliador["<b>Conciliador</b><br/><i>[Pessoa]</i><br/>Revisa e valida a<br/>sugestão da IA"]
  admin["<b>Administrador</b><br/><i>[Pessoa]</i><br/>Acompanha estatísticas<br/>e desempenho"]

  concilia["<b>Concilia IA</b><br/><i>[Sistema]</i><br/>Consulta normas da ANS e contratos,<br/>aplica IA e sugere a estratégia de<br/>conciliação. Decisão final humana."]

  llm["<b>Provedor de LLM</b><br/><i>[Sistema externo]</i><br/>OpenAI / Anthropic Claude"]
  ans["<b>Base de Normas da ANS</b><br/><i>[Sistema externo]</i><br/>Normas e resoluções da ANS"]
  tjms["<b>Sistema do TJMS</b><br/><i>[Sistema externo]</i><br/>Destino dos casos não conciliados"]

  cidadao -->|"Registra e consulta<br/>HTTPS"| concilia
  servidor -->|"Cadastra pedidos<br/>HTTPS"| concilia
  conciliador -->|"Revisa e valida<br/>HTTPS"| concilia
  admin -->|"Consulta estatísticas<br/>HTTPS"| concilia
  concilia -->|"Solicita análise e sugestão<br/>HTTPS/JSON"| llm
  concilia -->|"Consulta e ingere normas<br/>HTTPS"| ans
  concilia -->|"Encaminha casos<br/>não conciliados"| tjms

  classDef person fill:#08427b,stroke:#052e56,color:#ffffff
  classDef system fill:#1168bd,stroke:#0b4884,color:#ffffff
  classDef external fill:#8c8c8c,stroke:#5e5e5e,color:#ffffff
  class cidadao,servidor,conciliador,admin person
  class concilia system
  class llm,ans,tjms external
```

## Notas

- **Escopo:** a Concilia IA é o sistema em foco; **LLM**, **normas da ANS** e
  **TJMS** são externos (caixa-preta).
- A meta institucional é **reduzir o encaminhamento ao Juizado**: casos resolvidos
  na conciliação não viram processo.
- Decisões relacionadas: [ADR-0008 (LLM)](../adr/0008-llm-multiprovedor.md),
  [ADR-0009 (validação humana)](../adr/0009-validacao-humana.md).
