# Architecture Decision Records (ADRs) — Concilia IA

Registro das decisões arquiteturais do MVP **Concilia IA**, construídas a partir
do documento `projeto MVP.pdf`. Cada ADR documenta uma decisão, suas alternativas
e consequências, seguindo o padrão [MADR](https://adr.github.io/madr/).

> **Status possíveis:** `Proposto` · `Aceito` · `Depreciado` · `Substituído por ADR-XXXX`

| ADR | Título | Status |
|-----|--------|--------|
| [0001](0001-api-rest-unica.md) | Arquitetura como única API REST (mono-serviço) | Aceito |
| [0002](0002-python-fastapi.md) | Python + FastAPI como stack da API | Aceito |
| [0003](0003-rest-json-openapi.md) | REST/JSON com documentação OpenAPI (Swagger) | Aceito |
| [0004](0004-autenticacao-jwt.md) | Autenticação e autorização via JWT | Aceito |
| [0005](0005-postgresql-sqlalchemy.md) | PostgreSQL + SQLAlchemy para persistência | Aceito |
| [0006](0006-alembic-migracoes.md) | Alembic para migração de schema | Aceito |
| [0007](0007-pgvector-rag.md) | pgvector para busca semântica das normas da ANS (RAG) | Aceito |
| [0008](0008-llm-multiprovedor.md) | Integração multiprovedor de LLM (OpenAI/Claude) | Aceito |
| [0009](0009-validacao-humana.md) | Validação humana obrigatória (human-in-the-loop) | Aceito |
| [0010](0010-armazenamento-documentos.md) | Armazenamento de documentos e contratos (upload) | Aceito |
| [0011](0011-docker.md) | Docker para empacotamento e ambiente reprodutível | Aceito |
| [0012](0012-explicabilidade-auditoria.md) | Explicabilidade e auditoria das decisões de IA | Aceito |

## Como adicionar um novo ADR

1. Copie o formato de um ADR existente (Status, Data, Contexto, Decisão,
   Alternativas, Consequências, Notas de implementação, Referências).
2. Numere sequencialmente (`00NN-titulo-curto.md`).
3. Nunca edite a decisão de um ADR aceito: crie um novo ADR que o **substitui** e
   marque o antigo como `Substituído por ADR-XXXX`.
4. Atualize esta tabela e a seção 9 de [`../arquitetura-c4.md`](../arquitetura-c4.md).
