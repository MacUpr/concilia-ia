# C4 — Nível 3: Componente (API REST)

Zoom na **API REST**, o container desenvolvido pelo time. Público: desenvolvedores.

> Notação: **flowchart** seguindo as convenções do C4. A fronteira tracejada é o
> container **API REST**; os elementos internos são componentes (não implantáveis
> isoladamente).

```mermaid
---
config:
  theme: base
  themeVariables:
    fontFamily: "Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: "13px"
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
    nodeSpacing: 45
    rankSpacing: 55
---
flowchart TB
  web["<b>Aplicação Web</b><br/><i>[Container: SPA Web]</i>"]
  llm["<b>Provedor de LLM</b><br/><i>[Sistema externo]</i><br/>OpenAI / Claude"]

  subgraph boundary["API REST — Python / FastAPI"]
    auth["<b>Autenticação</b><br/><i>[JWT / OAuth2]</i><br/>Login e controle de acesso"]
    cadastros["<b>Cadastros</b><br/><i>[FastAPI Router]</i><br/>Usuários, planos,<br/>operadoras e contratos"]
    solicit["<b>Solicitações</b><br/><i>[Service]</i><br/>Ciclo de vida do pedido"]
    upload["<b>Upload de Documentos</b><br/><i>[Service]</i><br/>Recebe e valida arquivos"]
    analise["<b>Motor de Análise</b><br/><i>[Orquestrador]</i><br/>Monta contexto, chama<br/>o LLM e gera a sugestão"]
    rag["<b>Busca Semântica</b><br/><i>[pgvector]</i><br/>Recupera normas e cláusulas"]
    llmgw["<b>Gateway de LLM</b><br/><i>[Adapter]</i><br/>Abstração multiprovedor"]
    repo["<b>Repositórios</b><br/><i>[SQLAlchemy]</i><br/>Persistência e auditoria"]
  end

  db[("<b>Banco de Dados</b><br/><i>[PostgreSQL + pgvector]</i>")]
  storage["<b>Object Storage</b><br/><i>[S3-compat]</i>"]

  web -->|"Autentica<br/>JSON/HTTPS"| auth
  web -->|"Gerencia cadastros"| cadastros
  web -->|"Cria e consulta pedidos"| solicit
  web -->|"Envia documentos"| upload
  web -->|"Solicita análise"| analise

  upload -->|"Armazena<br/>S3 API"| storage
  analise -->|"Recupera contexto"| rag
  rag -->|"Consulta embeddings"| repo
  analise -->|"Solicita sugestão"| llmgw
  llmgw -->|"Chama o modelo<br/>HTTPS/JSON"| llm
  cadastros -->|"Lê e escreve"| repo
  solicit -->|"Lê e escreve"| repo
  analise -->|"Persiste sugestão<br/>e auditoria"| repo
  repo -->|"Lê e escreve<br/>SQL"| db

  classDef external fill:#8c8c8c,stroke:#5e5e5e,color:#ffffff
  classDef container fill:#438dd5,stroke:#2e6295,color:#ffffff
  classDef component fill:#85bbf0,stroke:#5d82a8,color:#000000
  class web,db,storage container
  class llm external
  class auth,cadastros,solicit,upload,analise,rag,llmgw,repo component
  style boundary fill:none,stroke:#438dd5,stroke-width:2px,stroke-dasharray:6 4
```

| Componente | Papel | ADR |
|------------|-------|-----|
| **Autenticação** | Login e RBAC via JWT | [0004](../adr/0004-autenticacao-jwt.md) |
| **Cadastros / Solicitações** | CRUD e ciclo de vida dos pedidos | [0001](../adr/0001-api-rest-unica.md) |
| **Upload de Documentos** | Recebe contratos e documentos | [0010](../adr/0010-armazenamento-documentos.md) |
| **Motor de Análise** | Orquestra RAG + LLM + sugestão | [0008](../adr/0008-llm-multiprovedor.md), [0009](../adr/0009-validacao-humana.md) |
| **Busca Semântica** | Recupera normas da ANS e cláusulas | [0007](../adr/0007-pgvector-rag.md) |
| **Gateway de LLM** | Isola o provedor de IA | [0008](../adr/0008-llm-multiprovedor.md) |
| **Repositórios** | Persistência e auditoria | [0005](../adr/0005-postgresql-sqlalchemy.md), [0012](../adr/0012-explicabilidade-auditoria.md) |

## Notas

- Os **componentes** são módulos internos do container **API REST** — não são
  implantáveis isoladamente.
- O fluxo completo em execução está em
  [`c4-dynamic-conciliacao.md`](c4-dynamic-conciliacao.md).
