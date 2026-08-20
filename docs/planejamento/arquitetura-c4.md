# Arquitetura da Solução — Modelo C4 (Concilia IA)

> Visão geral da arquitetura da **Concilia IA**, a API inteligente de apoio à
> **conciliação em saúde suplementar** (CEJUSC / TJMS). Os diagramas seguem o
> **modelo C4** (Simon Brown), em **Mermaid**, com **um diagrama por arquivo** na
> pasta [`c4/`](c4/). Documento construído a partir do `projeto MVP.pdf`.

Este arquivo é o **índice e a narrativa** do modelo. Os diagramas estão em:

| Nível | Diagrama |
|-------|----------|
| 1 — Contexto | [`c4/c4-context.md`](c4/c4-context.md) |
| 2 — Container | [`c4/c4-containers.md`](c4/c4-containers.md) |
| 3 — Componente | [`c4/c4-components-api.md`](c4/c4-components-api.md) |
| Dinâmico | [`c4/c4-dynamic-conciliacao.md`](c4/c4-dynamic-conciliacao.md) |
| Deployment | [`c4/c4-deployment.md`](c4/c4-deployment.md) |

---

## 1. Problema e objetivo

Hoje a análise de pedidos de conciliação envolvendo planos de saúde é **manual**,
**demorada**, gera **decisões inconsistentes**, leva a **excesso de
judicialização** e há **dificuldade em consultar rapidamente as normas da ANS**.

A **Concilia IA** é uma API que **recebe a solicitação**, **interpreta o pedido**,
**consulta normas e contratos**, **aplica IA** e **sugere a melhor estratégia de
conciliação** — sempre com **validação humana** do conciliador.

**Metas do MVP:** tempo médio de análise inferior a 2 minutos, mais de 80% das
sugestões aceitas, redução dos processos encaminhados ao Juizado.

---

## 2. Atores e escopo

| Ator | Necessidade |
|------|-------------|
| **Cidadão / Beneficiário** | Receber uma solução rápida para o conflito com a operadora |
| **Servidor do CEJUSC** | Registrar pedidos com rapidez |
| **Conciliador** | Tomar decisões rápidas e fundamentadas |
| **Administrador** | Acompanhar estatísticas e desempenho |

**No escopo:** a API REST, suas regras de negócio, persistência, IA e
armazenamento de documentos. **Externos:** provedores de LLM, base de normas da
ANS e os sistemas institucionais do TJMS.

---

## 3. Drivers arquiteturais

| Driver | Por quê |
|--------|---------|
| **Confiabilidade da decisão** | A IA é probabilística; a decisão final precisa ser humana |
| **Fundamentação / Explicabilidade** | Toda sugestão deve citar normas da ANS e cláusulas do contrato |
| **Segurança e privacidade** | Dados de saúde são sensíveis |
| **Rastreabilidade / Auditoria** | Registrar quem decidiu o quê e com base em quê |
| **Padronização** | Reduzir inconsistência entre conciliadores |
| **Reprodutibilidade** | Mesmo comportamento em qualquer ambiente |

---

## 4. Nível 1 — Contexto

A Concilia IA como uma unidade e suas relações com pessoas e sistemas externos
(**LLM**, **normas da ANS** e **TJMS**, tratados como caixa-preta).

➡ Diagrama: [`c4/c4-context.md`](c4/c4-context.md)

---

## 5. Nível 2 — Container

Blocos executáveis e de dados da solução.

➡ Diagrama: [`c4/c4-containers.md`](c4/c4-containers.md)

| Container | Tecnologia | Responsabilidade | ADR |
|-----------|-----------|------------------|-----|
| **Aplicação Web** | SPA Web | Interface das telas do MVP | — |
| **API REST** | Python / FastAPI | Endpoints, autenticação, regras, orquestração da IA | [0001](adr/0001-api-rest-unica.md), [0002](adr/0002-python-fastapi.md), [0003](adr/0003-rest-json-openapi.md) |
| **Banco de Dados** | PostgreSQL + pgvector | Persistência, auditoria e busca semântica | [0005](adr/0005-postgresql-sqlalchemy.md), [0007](adr/0007-pgvector-rag.md) |
| **Armazenamento de Documentos** | Object Storage (S3) | Contratos e documentos do upload | [0010](adr/0010-armazenamento-documentos.md) |

---

## 6. Nível 3 — Componente (API REST)

Estrutura interna da API REST — o container desenvolvido pelo time.

➡ Diagrama: [`c4/c4-components-api.md`](c4/c4-components-api.md)

| Componente | Papel | ADR |
|------------|-------|-----|
| **Autenticação** | Login e RBAC via JWT | [0004](adr/0004-autenticacao-jwt.md) |
| **Cadastros / Solicitações** | CRUD e ciclo de vida dos pedidos | [0001](adr/0001-api-rest-unica.md) |
| **Upload de Documentos** | Recebe contratos e documentos | [0010](adr/0010-armazenamento-documentos.md) |
| **Motor de Análise** | Orquestra RAG + LLM + sugestão | [0008](adr/0008-llm-multiprovedor.md), [0009](adr/0009-validacao-humana.md) |
| **Busca Semântica** | Recupera normas da ANS e cláusulas | [0007](adr/0007-pgvector-rag.md) |
| **Gateway de LLM** | Isola o provedor de IA | [0008](adr/0008-llm-multiprovedor.md) |
| **Repositórios** | Persistência e auditoria | [0005](adr/0005-postgresql-sqlalchemy.md), [0012](adr/0012-explicabilidade-auditoria.md) |

---

## 7. Fluxo principal (pedido → conciliação)

Sequência numerada do registro do pedido até a validação humana. A sugestão nasce
**`PENDENTE`** e só vira decisão após a validação do conciliador; a sugestão
original e a decisão são **auditadas**.

➡ Diagrama: [`c4/c4-dynamic-conciliacao.md`](c4/c4-dynamic-conciliacao.md)

Decisões: [ADR-0009](adr/0009-validacao-humana.md),
[ADR-0012](adr/0012-explicabilidade-auditoria.md).

---

## 8. Deployment (produção)

Componentes empacotados em **contêineres Docker**; API _stateless_ e replicável
atrás de _reverse proxy_.

➡ Diagrama: [`c4/c4-deployment.md`](c4/c4-deployment.md)

Decisões: [ADR-0011](adr/0011-docker.md), [ADR-0006](adr/0006-alembic-migracoes.md).

---

## 9. Requisitos Não Funcionais

| RNF | Como a arquitetura atende |
|-----|---------------------------|
| **Segurança** | TLS, JWT/RBAC, dados sensíveis protegidos ([0004](adr/0004-autenticacao-jwt.md)) |
| **Confiabilidade da decisão** | Validação humana obrigatória ([0009](adr/0009-validacao-humana.md)) |
| **Fundamentação** | RAG com normas da ANS via pgvector ([0007](adr/0007-pgvector-rag.md)) |
| **Auditabilidade** | Trilha de auditoria no PostgreSQL ([0012](adr/0012-explicabilidade-auditoria.md)) |
| **Portabilidade de IA** | Gateway multiprovedor ([0008](adr/0008-llm-multiprovedor.md)) |
| **Reprodutibilidade** | Containerização com Docker ([0011](adr/0011-docker.md)) |
| **Evolução do schema** | Migrações versionadas com Alembic ([0006](adr/0006-alembic-migracoes.md)) |

---

## 10. Decisões Arquiteturais (ADRs)

O **porquê** de cada decisão está registrado em [`adr/`](adr/) — ver o
[índice de ADRs](adr/README.md).

---

## Referências

- Simon Brown — **C4 model** (https://c4model.com)
- Documento-base: `projeto MVP.pdf`
