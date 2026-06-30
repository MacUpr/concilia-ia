# Architecture Decision Records (ADRs)

Registro das decisões arquiteturais da **API de Conciliação com IA**. Cada ADR
documenta uma decisão estrutural, suas alternativas e consequências, seguindo o
padrão [MADR](https://adr.github.io/madr/).

> **Status possíveis:** `Proposto` · `Aceito` · `Depreciado` · `Substituído por ADR-XXXX`

| ADR | Título | Status |
|-----|--------|--------|
| [0001](0001-aplicacao-como-api-rest-unica.md) | Aplicação como única API REST (mono-serviço) | Aceito |
| [0002](0002-python-fastapi.md) | Python + FastAPI como stack da API | Aceito |
| [0003](0003-abstracao-multiprovedor-llm.md) | Abstração multiprovedor de LLM | Aceito |
| [0004](0004-validacao-humana-obrigatoria.md) | Validação humana obrigatória (human-in-the-loop) | Aceito |
| [0005](0005-postgresql-persistencia-e-auditoria.md) | PostgreSQL para persistência e auditoria | Aceito |
| [0006](0006-redis-cache-e-fila.md) | Redis para cache e fila | Aceito |
| [0007](0007-processamento-assincrono-de-ia.md) | Processamento assíncrono de IA (fila + worker) | Aceito |
| [0008](0008-rest-json-como-estilo-de-api.md) | REST/JSON como estilo de API | Aceito |
| [0009](0009-protecao-de-dados-de-saude-e-lgpd.md) | Proteção de dados de saúde e LGPD | Aceito |
| [0010](0010-observabilidade.md) | Observabilidade (logs, métricas, tracing) | Proposto |

## Como adicionar um novo ADR

1. Copie o formato de um ADR existente (cabeçalho: Status, Data, Contexto,
   Decisão, Alternativas, Consequências).
2. Numere sequencialmente (`00NN-titulo-curto.md`).
3. Nunca edite a decisão de um ADR aceito: crie um novo ADR que o **substitui**
   e atualize o status do antigo para `Substituído por ADR-XXXX`.
4. Atualize esta tabela e a seção 11 de [`../arquitetura.md`](../arquitetura.md).
