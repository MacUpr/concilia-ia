# C4 — Deployment: Produção (Docker)

Infraestrutura de implantação em **produção**, com os componentes empacotados em
**contêineres Docker**. Público: DevOps.

> Notação: **flowchart** seguindo as convenções do C4. Cada caixa tracejada é um
> nó de implantação (_deployment node_).

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
  subgraph device["Navegador Web"]
    web["<b>Aplicação Web</b><br/><i>[SPA Web]</i><br/>Interface do usuário"]
  end

  subgraph cluster["Servidor / Cluster de Contêineres — Docker"]
    proxy["<b>Reverse Proxy</b><br/><i>[Nginx]</i><br/>Terminação TLS e roteamento"]
    api["<b>API REST</b><br/><i>[Python / FastAPI]</i><br/>Endpoints, regras e IA"]
    db[("<b>Banco de Dados</b><br/><i>[PostgreSQL + pgvector]</i><br/>Dados, auditoria e embeddings")]
    storage["<b>Armazenamento de Documentos</b><br/><i>[MinIO / S3]</i><br/>Contratos e documentos"]
  end

  llm["<b>Provedor de LLM</b><br/><i>[SaaS externo]</i><br/>OpenAI / Claude"]

  web -->|"Requisições da UI<br/>HTTPS"| proxy
  proxy -->|"Encaminha<br/>HTTP"| api
  api -->|"Lê e escreve<br/>SQL/TCP"| db
  api -->|"Armazena e recupera<br/>S3 API"| storage
  api -->|"Solicita análise<br/>HTTPS/JSON"| llm

  classDef container fill:#438dd5,stroke:#2e6295,color:#ffffff
  classDef external fill:#8c8c8c,stroke:#5e5e5e,color:#ffffff
  class web,proxy,api,db,storage container
  class llm external
  style device fill:none,stroke:#8c8c8c,stroke-width:2px,stroke-dasharray:6 4
  style cluster fill:none,stroke:#1168bd,stroke-width:2px,stroke-dasharray:6 4
```

## Notas

- **Empacotamento com Docker** — ver [ADR-0011](../adr/0011-docker.md). Em
  desenvolvimento, os mesmos serviços sobem via **Docker Compose**.
- A **API é _stateless_** e pode ser replicada horizontalmente atrás do _reverse
  proxy_; o estado fica no **PostgreSQL** e no **object storage**.
- **Migrações Alembic** rodam como passo do _deploy_, antes de subir a API — ver
  [ADR-0006](../adr/0006-alembic-migracoes.md).
