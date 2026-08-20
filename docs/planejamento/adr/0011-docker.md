# ADR-0011: Docker para empacotamento e ambiente reprodutível

## Status

Aceito

## Data

2026-07-14

## Contexto

A solução é composta por múltiplos componentes que precisam de ambientes
**consistentes** entre desenvolvimento e produção: **API REST**, **PostgreSQL**
(com pgvector) e **object storage**. Python exige controle **reprodutível** de
dependências e versões. É preciso facilitar o _onboarding_ do time e padronizar o
_deploy_.

## Decisão

**Containerizar** os componentes com **Docker**. A aplicação tem uma **imagem**
própria, com _build_ reprodutível a partir do _lockfile_. Usar **Docker Compose**
para orquestrar o ambiente local (API, PostgreSQL, object storage).

## Alternativas Consideradas

### Alternativa 1: Deploy direto no host (virtualenv + systemd)

- **Descrição**: Rodar a aplicação diretamente no SO do servidor.
- **Prós**: Simples; sem camada de container.
- **Contras**: _"funciona na minha máquina"_; _drift_ de ambiente.
- **Por que rejeitada**: Reprodutibilidade insuficiente.

### Alternativa 2: Buildpacks / PaaS sem Docker explícito

- **Descrição**: Deixar a plataforma empacotar a aplicação.
- **Prós**: Menos configuração inicial.
- **Contras**: Menor controle e transparência; _lock-in_ de plataforma.
- **Por que rejeitada**: Menos portável; preferimos um artefato de container padrão.

## Consequências

### Positivas

- **Paridade dev/prod**; _onboarding_ rápido (`docker compose up`).
- Portável para qualquer orquestrador (ex.: Kubernetes) em produção.
- Base para escalar réplicas da API de forma horizontal.

### Negativas

- Curva de aprendizado de Docker/Compose.
- Imagens precisam ser mantidas e atualizadas (segurança).

### Riscos

- Imagens com vulnerabilidades → _scan_ de imagem, base **slim** e atualização
  periódica.

## Notas de Implementação

- `Dockerfile` **multi-stage**; base _slim_; usuário **não-root**; `HEALTHCHECK`.
- **Docker Compose** para desenvolvimento.
- As migrações ([ADR-0006](0006-alembic-migracoes.md)) rodam como passo do
  _deploy_ antes de subir a aplicação.

## Referências

- [arquitetura-c4.md — Seção 5](../arquitetura-c4.md)
- [ADR-0002 — Python + FastAPI](0002-python-fastapi.md)
- [ADR-0006 — Alembic para migrações](0006-alembic-migracoes.md)
