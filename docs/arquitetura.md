# Visões Arquiteturais — API de Conciliação com IA

> Documento de visões arquiteturais da **API de Conciliação com IA**, serviço de
> apoio à resolução de demandas de **saúde suplementar** antes da judicialização,
> no contexto do **CEJUSC / TJMS** (Tribunal de Justiça de Mato Grosso do Sul).
>
> Modelo de representação: **C4** (Context, Container e Component, com visões
> Dinâmica e de Implantação complementares). Para garantir leitura clara e bom
> roteamento automático das setas, os diagramas usam a notação **flowchart** do
> Mermaid (e **sequence** na visão dinâmica), seguindo os níveis do C4. São
> versionados junto ao código, acompanhando a evolução do projeto.

---

## Identificação

**Projeto:** Pedido de Conciliação — Saúde Suplementar (TJMS)

**Grupo 02 — Integrantes**

| # | Nome |
|---|------|
| 1 | Eraldo Júnior |
| 2 | Suelen Maciel |
| 3 | Cleiton Carlos da Silva |
| 4 | Filipe Ferreira Falco |
| 5 | Luiz Eduardo Dos Santos Sousa |
| 6 | Abellard Christley Mainviel |

---

## 1. Introdução

A judicialização de demandas de **saúde suplementar** (negativas de cobertura,
autorizações de procedimentos, reembolsos) sobrecarrega o Judiciário. O CEJUSC
(Centro Judiciário de Solução de Conflitos e Cidadania) atua na **conciliação
pré-processual**: busca-se resolver o conflito entre cidadão e operadora de
plano de saúde **antes** de virar processo.

A **API de Conciliação com IA** é o serviço de back-end que apoia esse processo.
Ela recebe a reclamação do cidadão, **classifica e prioriza** a demanda e **gera
sugestões de conciliação** com apoio de modelos de linguagem (LLMs). As sugestões
**nunca** são aplicadas automaticamente: passam pela **validação humana** de um
conciliador do CEJUSC, que mantém o controle da decisão.

Este documento descreve a arquitetura **apenas da API REST** — o componente que o
grupo desenvolve. Interfaces de usuário (web/mobile), o Sistema TJMS e os
provedores de LLM são tratados como **sistemas externos**.

---

## 2. Escopo e delimitação

| Dentro do escopo (o que construímos) | Fora do escopo (externo) |
|--------------------------------------|--------------------------|
| API REST de processamento de IA | Aplicação Web / Frontend (consumidor) |
| Regras de negócio da conciliação | Provedores de LLM (Anthropic / OpenAI) |
| Classificação e geração de sugestões | Sistema TJMS (processos institucionais) |
| Persistência, cache e fila assíncrona | Autenticação federada / identidade dos usuários |
| Trilha de auditoria das decisões | Infraestrutura de nuvem gerenciada |

A aplicação é, deliberadamente, **uma única API REST** que concentra todo o
processamento de IA (ver [ADR-0001](adr/0001-aplicacao-como-api-rest-unica.md)).

---

## 3. Drivers arquiteturais

Os requisitos não funcionais (RNFs) que mais moldam a arquitetura:

| Driver | Por quê |
|--------|---------|
| **Confiabilidade da decisão** | A IA é probabilística e pode errar/alucinar; a decisão final precisa ser humana. |
| **Segurança e privacidade** | Dados de saúde são sensíveis (LGPD, art. 11 — dados sensíveis). |
| **Auditabilidade** | É preciso rastrear quem decidiu o quê e com base em qual sugestão da IA. |
| **Resiliência a dependências externas** | LLMs e TJMS são externos, com latência e indisponibilidade variáveis. |
| **Escalabilidade** | Volume de demandas pode crescer e oscilar (picos). |
| **Portabilidade de fornecedor de IA** | Evitar lock-in em um único provedor de LLM. |

---

## 4. Visão de Contexto (C4 — Nível 1)

Mostra a API como uma unidade central e suas interações com pessoas e sistemas
externos.

```mermaid
flowchart LR
  cliente["<b>Cliente</b><br/><i>[Pessoa]</i><br/>Beneficiário de plano de saúde<br/>que registra a reclamação"]
  conciliador["<b>Conciliador CEJUSC</b><br/><i>[Pessoa]</i><br/>Revisa e valida as<br/>sugestões de conciliação"]
  frontend["<b>Aplicação Web</b><br/><i>[Sistema externo]</i><br/>Interface (fora do escopo)<br/>que consome a API REST"]
  api["<b>API de Conciliação com IA</b><br/><i>[Sistema]</i><br/>Classifica reclamações e gera<br/>sugestões com apoio de LLMs"]
  llm["<b>Provedores de LLM</b><br/><i>[Sistema externo]</i><br/>Anthropic Claude / OpenAI"]
  tjms["<b>Sistema TJMS</b><br/><i>[Sistema externo]</i><br/>Processos e dados institucionais"]

  cliente -->|"Registra e acompanha<br/>HTTPS"| frontend
  conciliador -->|"Revisa e valida<br/>HTTPS"| frontend
  frontend -->|"Consome<br/>JSON/HTTPS"| api
  api -->|"Classificação e geração<br/>JSON/HTTPS"| llm
  api -->|"Integra dados do processo<br/>JSON/HTTPS"| tjms

  classDef person fill:#08427b,stroke:#052e56,color:#ffffff
  classDef system fill:#1168bd,stroke:#0b4884,color:#ffffff
  classDef external fill:#8c8c8c,stroke:#5e5e5e,color:#ffffff
  class cliente,conciliador person
  class api system
  class frontend,llm,tjms external
```

**Atores**

- **Cliente** — beneficiário do plano de saúde; registra a reclamação e acompanha
  o andamento (via Aplicação Web).
- **Conciliador CEJUSC** — revisa e **valida** as propostas geradas pela IA,
  garantindo o controle humano.

**Sistemas externos**

- **Aplicação Web** — front-end consumidor da API (desenvolvido por outra
  frente/equipe; fora do escopo deste documento).
- **Provedores de LLM** — Anthropic Claude / OpenAI; executam a análise
  inteligente. Acessados via camada de abstração (ver
  [ADR-0003](adr/0003-abstracao-multiprovedor-llm.md)).
- **Sistema TJMS** — integração com dados institucionais e processos.

---

## 5. Visão de Containers (C4 — Nível 2)

Detalha os blocos tecnológicos da API e suas responsabilidades. Todos os
containers internos compõem **um único serviço lógico** — a fronteira do sistema.

```mermaid
flowchart TB
  cliente["<b>Cliente</b><br/><i>[Pessoa]</i><br/>Registra reclamação"]
  conciliador["<b>Conciliador CEJUSC</b><br/><i>[Pessoa]</i><br/>Valida conciliação"]
  frontend["<b>Aplicação Web</b><br/><i>[Sistema externo]</i><br/>Consome a API (fora do escopo)"]
  llm["<b>Provedores de LLM</b><br/><i>[Sistema externo]</i><br/>Anthropic / OpenAI"]
  tjms["<b>Sistema TJMS</b><br/><i>[Sistema externo]</i><br/>Dados institucionais"]

  subgraph api_boundary["API de Conciliação com IA"]
    rest["<b>API REST</b><br/><i>[Python · FastAPI]</i><br/>Endpoints, validação,<br/>regras e orquestração da IA"]
    worker["<b>Worker de IA</b><br/><i>[Python · Celery]</i><br/>Análises de IA assíncronas"]
    db[("<b>Banco de Dados</b><br/><i>[PostgreSQL]</i><br/>Reclamações, decisões<br/>e trilha de auditoria")]
    cache[("<b>Cache e Fila</b><br/><i>[Redis]</i><br/>Cache e fila de tarefas")]
  end

  cliente -->|"Usa<br/>HTTPS"| frontend
  conciliador -->|"Usa<br/>HTTPS"| frontend
  frontend -->|"Chama<br/>JSON/HTTPS"| rest
  rest -->|"Lê e escreve<br/>SQL / asyncpg"| db
  rest -->|"Cacheia e enfileira<br/>Redis"| cache
  worker -->|"Consome tarefas<br/>Redis"| cache
  worker -->|"Solicita análise<br/>JSON/HTTPS"| llm
  worker -->|"Persiste resultados<br/>SQL / asyncpg"| db
  rest -->|"Integra<br/>JSON/HTTPS"| tjms

  classDef person fill:#08427b,stroke:#052e56,color:#ffffff
  classDef container fill:#1168bd,stroke:#0b4884,color:#ffffff
  classDef external fill:#8c8c8c,stroke:#5e5e5e,color:#ffffff
  class cliente,conciliador person
  class rest,worker,db,cache container
  class frontend,llm,tjms external
  style api_boundary fill:none,stroke:#1168bd,stroke-width:2px,stroke-dasharray:6 4
```

| Container | Tecnologia | Responsabilidade | ADR |
|-----------|-----------|------------------|-----|
| **API REST** | Python / FastAPI | Endpoints REST, validação (Pydantic), autenticação, orquestração das regras de negócio | [0002](adr/0002-python-fastapi.md), [0008](adr/0008-rest-json-como-estilo-de-api.md) |
| **Worker de IA** | Python / Celery | Executa chamadas de LLM (longas) de forma assíncrona, fora do ciclo HTTP | [0007](adr/0007-processamento-assincrono-de-ia.md) |
| **Banco de Dados** | PostgreSQL | Persistência relacional e trilha de auditoria | [0005](adr/0005-postgresql-persistencia-e-auditoria.md) |
| **Cache e Fila** | Redis | Cache de respostas/consultas e _broker_ da fila assíncrona | [0006](adr/0006-redis-cache-e-fila.md) |

> O processamento de IA é assíncrono porque chamadas a LLMs podem levar de
> segundos a dezenas de segundos. A API REST responde rápido (enfileira o
> trabalho) e o Worker processa em segundo plano.

---

## 6. Visão de Componentes (C4 — Nível 3)

Detalha a estrutura interna do código que compõe o serviço. Os componentes de
domínio (Classificação, Sugestão, Gateway de LLM) são **compartilhados** entre a
API REST e o Worker de IA — é o mesmo código, com pontos de entrada diferentes.

```mermaid
flowchart TB
  frontend["<b>Aplicação Web</b><br/><i>[Sistema externo]</i><br/>Consumidor da API"]
  llm["<b>Provedores de LLM</b><br/><i>[Sistema externo]</i><br/>Anthropic / OpenAI"]
  tjms["<b>Sistema TJMS</b><br/><i>[Sistema externo]</i><br/>Dados institucionais"]
  db[("<b>Banco de Dados</b><br/><i>[PostgreSQL]</i>")]
  cache[("<b>Cache e Fila</b><br/><i>[Redis]</i>")]

  subgraph svc["Serviço de Conciliação com IA"]
    router["<b>Camada de Endpoints</b><br/><i>[FastAPI Routers]</i><br/>Rotas, autenticação e validação"]
    conciliacao["<b>Serviço de Conciliação</b><br/><i>[Python]</i><br/>Orquestra o fluxo e as regras"]
    classificacao["<b>Serviço de Classificação</b><br/><i>[Python]</i><br/>Classifica e prioriza"]
    sugestao["<b>Serviço de Sugestão</b><br/><i>[Python]</i><br/>Gera propostas de conciliação"]
    llmgw["<b>Gateway de LLM</b><br/><i>[Python · Strategy]</i><br/>Abstração multiprovedor"]
    repo["<b>Repositórios</b><br/><i>[SQLAlchemy]</i><br/>Acesso a dados e persistência"]
    tjmsclient["<b>Cliente TJMS</b><br/><i>[httpx]</i><br/>Integração com o TJMS"]
    audit["<b>Auditoria</b><br/><i>[Python]</i><br/>Registra decisões e ações"]
  end

  frontend -->|"Chama<br/>JSON/HTTPS"| router
  router -->|"Invoca"| conciliacao
  conciliacao -->|"Solicita classificação"| classificacao
  conciliacao -->|"Solicita sugestão"| sugestao
  classificacao -->|"Usa"| llmgw
  sugestao -->|"Usa"| llmgw
  conciliacao -->|"Lê e escreve"| repo
  conciliacao -->|"Consulta processo"| tjmsclient
  conciliacao -->|"Registra decisões"| audit
  audit -->|"Persiste via"| repo
  repo -->|"SQL"| db
  llmgw -->|"Cacheia respostas"| cache
  llmgw -->|"Chama<br/>JSON/HTTPS"| llm
  tjmsclient -->|"JSON/HTTPS"| tjms

  classDef component fill:#1168bd,stroke:#0b4884,color:#ffffff
  classDef external fill:#8c8c8c,stroke:#5e5e5e,color:#ffffff
  class router,conciliacao,classificacao,sugestao,llmgw,repo,tjmsclient,audit component
  class frontend,llm,tjms,db,cache external
  style svc fill:none,stroke:#1168bd,stroke-width:2px,stroke-dasharray:6 4
```

| Componente | Responsabilidade |
|-----------|------------------|
| **Camada de Endpoints** | Expõe as rotas REST, valida payloads, aplica autenticação/autorização. |
| **Serviço de Conciliação** | Orquestra o caso de uso: persiste a reclamação, dispara a análise de IA, consolida a sugestão e registra a decisão validada. |
| **Serviço de Classificação** | Classifica o tipo da demanda (ex.: negativa de procedimento, reembolso) e atribui prioridade. |
| **Serviço de Sugestão** | Gera a proposta de conciliação textual a partir do contexto da reclamação. |
| **Gateway de LLM** | Isola o resto do sistema do provedor de IA; permite trocar Anthropic↔OpenAI sem afetar o domínio ([ADR-0003](adr/0003-abstracao-multiprovedor-llm.md)). |
| **Repositórios** | Encapsulam o acesso ao PostgreSQL. |
| **Cliente TJMS** | Encapsula a integração HTTP com o Sistema TJMS. |
| **Auditoria** | Registra eventos de decisão para rastreabilidade ([ADR-0009](adr/0009-protecao-de-dados-de-saude-e-lgpd.md)). |

---

## 7. Visão Dinâmica — fluxo de conciliação (C4 Dynamic)

Cenário principal (+1, na linguagem do 4+1): da reclamação à decisão validada,
evidenciando o **controle humano**.

```mermaid
sequenceDiagram
  autonumber
  actor F as Aplicação Web
  participant R as API REST
  participant Q as Cache / Fila · Redis
  participant W as Worker de IA
  participant D as Banco · PostgreSQL
  participant L as Provedores de LLM

  F->>R: POST /reclamacoes (registra)
  R->>D: Persiste reclamação
  R->>Q: Enfileira análise de IA
  R-->>F: 202 Accepted
  Q->>W: Entrega a tarefa
  W->>L: Classifica e gera sugestão
  L-->>W: Classificação + sugestão
  W->>D: Persiste sugestão (status PENDENTE)
  Note over F,D: Revisão humana obrigatória
  F->>R: GET /sugestoes (conciliador revisa)
  R->>D: Consulta sugestões
  D-->>R: Sugestões PENDENTES
  R-->>F: Lista de sugestões
  F->>R: POST /sugestoes/:id/validar (aprova ou ajusta)
  R->>D: Registra decisão + auditoria
  R-->>F: 200 OK
```

Observe a **revisão humana obrigatória** destacada no diagrama (entre a persistência
da sugestão e a validação): a sugestão fica `PENDENTE` até o conciliador aprovar ou
ajustar ([ADR-0004](adr/0004-validacao-humana-obrigatoria.md)).

---

## 8. Visão de Implantação (C4 Deployment)

```mermaid
flowchart TB
  subgraph cloud["☁️ Provedor de Nuvem — Plataforma de Containers"]
    subgraph runtime["Container Runtime / Kubernetes (Linux)"]
      rest["<b>API REST</b><br/><i>[FastAPI · Uvicorn]</i><br/>Réplicas atrás de balanceador"]
      worker["<b>Worker de IA</b><br/><i>[Celery]</i><br/>Processa a fila de IA"]
    end
    subgraph managed["Serviços Gerenciados"]
      db[("<b>PostgreSQL</b><br/><i>Banco gerenciado</i>")]
      cache[("<b>Redis</b><br/><i>Cache gerenciado</i>")]
    end
  end
  llm["<b>Provedores de LLM</b><br/><i>[Sistema externo]</i><br/>Anthropic / OpenAI"]
  tjms["<b>Sistema TJMS</b><br/><i>[Sistema externo]</i><br/>Institucional"]

  rest -->|"Lê/escreve · TLS"| db
  rest -->|"Cache/fila · TLS"| cache
  worker -->|"Consome · TLS"| cache
  worker -->|"Chama · HTTPS"| llm
  rest -->|"Integra · HTTPS"| tjms

  classDef node fill:#1168bd,stroke:#0b4884,color:#ffffff
  classDef external fill:#8c8c8c,stroke:#5e5e5e,color:#ffffff
  class rest,worker,db,cache node
  class llm,tjms external
  style cloud fill:none,stroke:#7f8c9a,stroke-width:1px
  style runtime fill:none,stroke:#1168bd,stroke-width:2px,stroke-dasharray:6 4
  style managed fill:none,stroke:#1168bd,stroke-width:2px,stroke-dasharray:6 4
```

A API REST escala horizontalmente (réplicas _stateless_ atrás de balanceador); o
Worker de IA escala de forma independente conforme a profundidade da fila. Banco
e cache são serviços gerenciados.

---

## 9. Uso da Inteligência Artificial e controle humano

A IA é **suporte ao processo decisório**, aplicada em:

- **Classificação automática** das reclamações (tipo e prioridade);
- **Geração de sugestões** de conciliação;
- **Apoio à priorização** das demandas.

**Salvaguardas (decisão de projeto):**

- A IA é probabilística e pode apresentar erros/alucinações.
- A **decisão final é sempre do conciliador** — sugestões ficam `PENDENTE` até
  validação humana.
- Toda decisão é **auditada** (sugestão original da IA + ação do conciliador).

Ver [ADR-0004](adr/0004-validacao-humana-obrigatoria.md).

---

## 10. Requisitos Não Funcionais (RNFs)

| RNF | Como a arquitetura atende |
|-----|---------------------------|
| **Performance** | Resposta rápida da API via processamento assíncrono + cache (Redis). |
| **Segurança** | TLS, dados de saúde criptografados, controle de acesso, segredos de API protegidos ([ADR-0009](adr/0009-protecao-de-dados-de-saude-e-lgpd.md)). |
| **Disponibilidade** | API _stateless_ replicável; degradação controlada quando o LLM/TJMS falham. |
| **Escalabilidade** | API e Worker escalam de forma independente. |
| **Auditabilidade** | Trilha de auditoria persistida no PostgreSQL. |
| **Portabilidade** | Gateway de LLM multiprovedor evita _lock-in_ ([ADR-0003](adr/0003-abstracao-multiprovedor-llm.md)). |
| **Observabilidade** | Logs estruturados, métricas e _tracing_ ([ADR-0010](adr/0010-observabilidade.md)). |

---

## 11. Decisões Arquiteturais (ADRs)

Cada decisão estrutural está registrada como um ADR em [`docs/adr/`](adr/).

| ADR | Decisão | Status |
|-----|---------|--------|
| [0001](adr/0001-aplicacao-como-api-rest-unica.md) | Aplicação como **única API REST** (mono-serviço) | Aceito |
| [0002](adr/0002-python-fastapi.md) | **Python + FastAPI** como stack da API | Aceito |
| [0003](adr/0003-abstracao-multiprovedor-llm.md) | **Abstração multiprovedor** de LLM (Anthropic/OpenAI) | Aceito |
| [0004](adr/0004-validacao-humana-obrigatoria.md) | **Validação humana obrigatória** (human-in-the-loop) | Aceito |
| [0005](adr/0005-postgresql-persistencia-e-auditoria.md) | **PostgreSQL** para persistência e auditoria | Aceito |
| [0006](adr/0006-redis-cache-e-fila.md) | **Redis** para cache e fila | Aceito |
| [0007](adr/0007-processamento-assincrono-de-ia.md) | **Processamento assíncrono** de IA (fila + worker) | Aceito |
| [0008](adr/0008-rest-json-como-estilo-de-api.md) | **REST/JSON** como estilo de API | Aceito |
| [0009](adr/0009-protecao-de-dados-de-saude-e-lgpd.md) | **Proteção de dados de saúde / LGPD** | Aceito |
| [0010](adr/0010-observabilidade.md) | **Observabilidade** (logs, métricas, _tracing_) | Proposto |

---

## 12. Trade-offs

| Decisão | Benefício | Custo / Risco |
|---------|-----------|----------------|
| Uso de IA | Automação e ganho de eficiência | Erros/alucinação → mitigado por validação humana |
| API REST única | Simplicidade operacional, menos _overhead_ | Acoplamento interno maior que microsserviços |
| Abstração de LLM | Evita _lock-in_, troca de provedor | Camada extra, menor denominador comum entre APIs |
| Processamento assíncrono | API responsiva, resiliente a latência do LLM | Complexidade (fila, _eventual consistency_) |
| Cache (Redis) | Performance, menos chamadas repetidas | Consistência/_staleness_ do dado em cache |
| Integração externa (TJMS) | Reúso de dados institucionais | Dependência de disponibilidade externa |

---

## 13. Riscos técnicos e mitigação

| Risco | Mitigação |
|-------|-----------|
| Respostas incorretas da IA | Validação humana obrigatória + auditoria |
| Latência/indisponibilidade do LLM | Processamento assíncrono, _timeouts_, _retry_, _fallback_ entre provedores |
| Indisponibilidade do TJMS | Degradação controlada; reprocessamento posterior |
| Vazamento de dados sensíveis | Criptografia, controle de acesso, minimização de dados, LGPD |
| Custos de API de IA | Cache de respostas, escolha de modelo por tarefa, limites de uso |

---

## 14. Evolução do sistema

- Avaliação contínua da qualidade das sugestões (_feedback_ do conciliador → métricas).
- Observabilidade completa (logs, _tracing_ distribuído, métricas) — ver ADR-0010.
- Possível automação parcial de casos de baixa complexidade (sempre com revisão por amostragem).
- _Fine-tuning_ / RAG com base no histórico de conciliações.

---

## 15. Conclusão

A arquitetura equilibra **automação** e **controle humano**: a IA atua como
suporte, sem substituir a decisão do conciliador. Concentrar todo o processamento
em **uma única API REST** mantém a operação simples nesta fase do projeto, e a
separação clara de componentes — com o **Gateway de LLM** isolando o fornecedor de
IA e o **processamento assíncrono** absorvendo a latência externa — permite
evoluir o sistema com controle de riscos.

---

## Apêndice A — Diagramas legados (versão inicial)

As imagens abaixo representam a **primeira versão** da modelagem, que descrevia o
**sistema completo** (incluindo Frontend e back-end em Node.js). Foram mantidas
como histórico; as visões oficiais e atuais são os diagramas Mermaid acima
(API REST como sistema, em Python/FastAPI).

- ![Contexto (legado)](c4-context.png)
- ![Containers (legado)](c4-container.png)

---

## Referências

- Simon Brown — **C4 model** (https://c4model.com)
- ADRs do projeto — [`docs/adr/`](adr/)
- LGPD — Lei nº 13.709/2018 (dados pessoais sensíveis de saúde)
