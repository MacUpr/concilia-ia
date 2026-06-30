# ADR-0002: Python + FastAPI como stack da API

## Status

Aceito

## Date

2026-06-29

## Context

A aplicação é uma API REST cujo núcleo é o **processamento de IA** (integração com
LLMs, manipulação de texto, classificação). A escolha da linguagem/framework deve
favorecer produtividade, ecossistema de IA maduro e bom suporte a I/O assíncrono
(chamadas a LLMs são predominantemente _I/O bound_).

A modelagem inicial citava Node.js, mas o ecossistema de IA/LLM é mais maduro e
idiomático em Python (SDKs oficiais Anthropic/OpenAI, bibliotecas de NLP, validação
de dados).

## Decision

Usar **Python** com **FastAPI** para a API REST. Complementos do mesmo ecossistema:
**Pydantic** (validação/serialização), **Uvicorn/ASGI** (servidor assíncrono),
**SQLAlchemy** (ORM/repositórios) e **httpx** (cliente HTTP assíncrono para LLMs e
TJMS).

## Alternatives Considered

### Alternative 1: Node.js (TypeScript) + NestJS/Express

- **Description**: Stack JavaScript/TypeScript.
- **Pros**: Linguagem única se compartilhada com o front-end; bom desempenho I/O.
- **Cons**: Ecossistema de IA menos maduro; SDKs de LLM seguem o Python primeiro.
- **Why rejected**: A vantagem de IA pesa mais que a unificação de linguagem (front é externo).

### Alternative 2: Rust (Axum/Actix)

- **Description**: Stack de alta performance e baixo consumo.
- **Pros**: Desempenho e segurança de memória excelentes.
- **Cons**: Ecossistema de IA imaturo; maior esforço de desenvolvimento e integração.
- **Why rejected**: Custo de desenvolvimento alto; ganho de performance irrelevante para carga _I/O bound_.

## Consequences

### Positive

- Acesso direto a SDKs oficiais de LLM e ferramentas de NLP.
- FastAPI gera documentação OpenAPI/Swagger automaticamente.
- Validação robusta com Pydantic; suporte nativo a `async/await`.

### Negative

- Python tem desempenho de CPU inferior a Go/Rust (irrelevante para carga _I/O bound_).
- Necessário cuidado com GIL em tarefas CPU-bound → delegadas ao Worker/processos.

### Risks

- Gestão de dependências/ambiente → mitigado com _lockfile_ (Poetry/uv) e imagem de container reprodutível.

## Implementation Notes

- Servir com Uvicorn (workers ASGI) atrás de um _reverse proxy_.
- Habilitar a documentação OpenAPI automática do FastAPI para o front-end consumir.

## References

- [arquitetura.md — Seção 5 (Containers)](../arquitetura.md)
