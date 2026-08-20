# Planejamento Arquitetural — Concilia IA

> Planejamento arquitetural **construído do zero** a partir do documento
> **`projeto MVP.pdf`**, de forma independente. Descreve a arquitetura da solução
> (modelo **C4**) e as **decisões arquiteturais (ADRs)** do MVP de uma **API
> inteligente de apoio à conciliação em saúde suplementar** no contexto do
> **CEJUSC / TJMS**.

## Conteúdo

| Documento | Descrição |
|-----------|-----------|
| [`arquitetura-c4.md`](arquitetura-c4.md) | **Índice e narrativa** do modelo C4 (drivers, RNFs, ligação com ADRs) |
| [`c4/`](c4/) | Modelo **C4** — um diagrama por arquivo: Contexto, Container, Componente, Dinâmico e Deployment |
| [`adr/`](adr/) | **Architecture Decision Records** — decisões estruturais do MVP |

Diagramas do modelo C4 (em [`c4/`](c4/)):

| Nível | Arquivo |
|-------|---------|
| 1 — Contexto | [`c4/c4-context.md`](c4/c4-context.md) |
| 2 — Container | [`c4/c4-containers.md`](c4/c4-containers.md) |
| 3 — Componente | [`c4/c4-components-api.md`](c4/c4-components-api.md) |
| Dinâmico | [`c4/c4-dynamic-conciliacao.md`](c4/c4-dynamic-conciliacao.md) |
| Deployment | [`c4/c4-deployment.md`](c4/c4-deployment.md) |

## Visão geral

A solução — **Concilia IA** — é uma **API REST** que recebe pedidos de
conciliação, **consulta as normas da ANS** e os contratos das operadoras, **aplica
Inteligência Artificial** para sugerir a melhor estratégia de conciliação e
apresenta o resultado ao **conciliador**, que mantém a **decisão final**
(_human-in-the-loop_). O objetivo é **reduzir o tempo de análise**, **padronizar
as decisões** e **evitar a judicialização desnecessária**.

## Pilha tecnológica (do PDF)

Python · FastAPI · PostgreSQL · SQLAlchemy · Alembic · pgvector · Docker · JWT ·
Swagger/OpenAPI · OpenAI/Claude · GitHub.

## Como navegar

1. Comece pelo [modelo C4](arquitetura-c4.md) para entender a estrutura.
2. Consulte os [ADRs](adr/) para o **porquê** de cada decisão.
