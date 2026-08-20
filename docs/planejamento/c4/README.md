# Modelo C4 — Concilia IA

Documentação de arquitetura no **modelo C4** (Simon Brown), com **um diagrama por
arquivo** em **Mermaid**. Construído a partir do `projeto MVP.pdf`.

| Nível | Arquivo | Mostra | Audiência |
|-------|---------|--------|-----------|
| 1 — Contexto | [`c4-context.md`](c4-context.md) | Sistema + pessoas + sistemas externos | Todos |
| 2 — Container | [`c4-containers.md`](c4-containers.md) | Aplicações, banco e serviços | Técnica / PM |
| 3 — Componente | [`c4-components-api.md`](c4-components-api.md) | Internos da API REST | Desenvolvedores |
| Dinâmico | [`c4-dynamic-conciliacao.md`](c4-dynamic-conciliacao.md) | Fluxo pedido → conciliação (numerado) | Técnica |
| Deployment | [`c4-deployment.md`](c4-deployment.md) | Infraestrutura de produção (Docker) | DevOps |

> Visão geral, drivers, RNFs e ligação com os ADRs em
> [`../arquitetura-c4.md`](../arquitetura-c4.md).

## Legenda (aplicada a todos os diagramas)

| Notação | Significado |
|---------|-------------|
| **Pessoa** | Ator humano que usa o sistema |
| **Sistema** | O sistema em foco (Concilia IA) |
| **Sistema externo** | Sistema fora do escopo, tratado como caixa-preta |
| **Container** | Unidade executável/implantável (app, API, banco, storage) |
| **Componente** | Módulo interno de um container (não implantável isoladamente) |
| **Seta** | Fluxo unidirecional, rotulado com ação + tecnologia/protocolo |

## Convenções

- **Aliases consistentes** entre os níveis (`api`, `db`, `storage`, `llm`…).
- **Setas unidirecionais** com verbo de ação e protocolo.
- Sistemas externos como **caixa-preta** (sem detalhar internamente).
- O **porquê** de cada decisão fica nos [ADRs](../adr/); os diagramas mostram o
  **resultado** das decisões, não o processo.
