# C4 — Nível 2: Container (Concilia IA)

Detalha os blocos executáveis e de dados da solução. Público: técnico e produto.

> Notação: **flowchart** seguindo as convenções do C4. A fronteira tracejada é o
> sistema **Concilia IA**.

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
  cidadao["<b>Cidadão</b><br/><i>[Pessoa]</i>"]
  servidor["<b>Servidor do CEJUSC</b><br/><i>[Pessoa]</i>"]
  conciliador["<b>Conciliador</b><br/><i>[Pessoa]</i>"]
  admin["<b>Administrador</b><br/><i>[Pessoa]</i>"]

  subgraph boundary["Concilia IA"]
    web["<b>Aplicação Web</b><br/><i>[Container: SPA Web]</i><br/>Telas de login, dashboard,<br/>solicitação, upload e resultado"]
    api["<b>API REST</b><br/><i>[Container: Python / FastAPI]</i><br/>Autenticação JWT, regras,<br/>orquestração da IA e Swagger"]
    db[("<b>Banco de Dados</b><br/><i>[Container: PostgreSQL + pgvector]</i><br/>Dados, auditoria e embeddings")]
    storage["<b>Armazenamento de Documentos</b><br/><i>[Container: Object Storage S3]</i><br/>Contratos e documentos"]
  end

  llm["<b>Provedor de LLM</b><br/><i>[Sistema externo]</i><br/>OpenAI / Claude"]
  ans["<b>Base de Normas da ANS</b><br/><i>[Sistema externo]</i><br/>Normas e resoluções"]

  cidadao -->|"Usa<br/>HTTPS"| web
  servidor -->|"Usa<br/>HTTPS"| web
  conciliador -->|"Usa<br/>HTTPS"| web
  admin -->|"Usa<br/>HTTPS"| web
  web -->|"Consome endpoints<br/>JSON/HTTPS"| api
  api -->|"Lê e escreve<br/>SQL / SQLAlchemy"| db
  api -->|"Armazena e recupera<br/>S3 API"| storage
  api -->|"Solicita análise<br/>HTTPS/JSON"| llm
  api -->|"Consulta e ingere normas<br/>HTTPS"| ans

  classDef person fill:#08427b,stroke:#052e56,color:#ffffff
  classDef container fill:#438dd5,stroke:#2e6295,color:#ffffff
  classDef external fill:#8c8c8c,stroke:#5e5e5e,color:#ffffff
  class cidadao,servidor,conciliador,admin person
  class web,api,db,storage container
  class llm,ans external
  style boundary fill:none,stroke:#1168bd,stroke-width:2px,stroke-dasharray:6 4
```

| Container | Tecnologia | Responsabilidade | ADR |
|-----------|-----------|------------------|-----|
| **Aplicação Web** | SPA Web | Interface das telas do MVP (consome a API) | — |
| **API REST** | Python / FastAPI | Endpoints, autenticação, regras, orquestração da IA | [0001](../adr/0001-api-rest-unica.md), [0002](../adr/0002-python-fastapi.md), [0003](../adr/0003-rest-json-openapi.md) |
| **Banco de Dados** | PostgreSQL + pgvector | Persistência, auditoria e busca semântica | [0005](../adr/0005-postgresql-sqlalchemy.md), [0007](../adr/0007-pgvector-rag.md) |
| **Armazenamento de Documentos** | Object Storage (S3) | Contratos e documentos do upload | [0010](../adr/0010-armazenamento-documentos.md) |

## Notas

- A **API REST é única** (mono-serviço) — ver [ADR-0001](../adr/0001-api-rest-unica.md).
- O **TJMS** não aparece aqui: é relação de contexto (Nível 1), sem integração
  técnica em nível de container no MVP.
- Detalhamento interno da API em [`c4-components-api.md`](c4-components-api.md).
