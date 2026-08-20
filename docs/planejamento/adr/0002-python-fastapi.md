# ADR-0002: Python + FastAPI como stack da API

## Status

Aceito

## Data

2026-07-14

## Contexto

O núcleo do produto é o **processamento de IA**: integração com LLMs, manipulação
de texto (normas, contratos) e classificação. A escolha da linguagem/framework
deve favorecer **produtividade**, **ecossistema de IA maduro** e bom suporte a
**I/O assíncrono** (chamadas a LLMs são predominantemente _I/O bound_).

## Decisão

Usar **Python** com **FastAPI** para a API REST. Complementos do mesmo
ecossistema: **Pydantic** (validação/serialização), **Uvicorn/ASGI** (servidor
assíncrono), **SQLAlchemy** (ORM) e um cliente HTTP assíncrono (**httpx**) para as
integrações externas.

## Alternativas Consideradas

### Alternativa 1: Node.js (TypeScript)

- **Descrição**: Stack JavaScript/TypeScript.
- **Prós**: Linguagem única com o front-end; bom desempenho de I/O.
- **Contras**: Ecossistema de IA/LLM menos maduro; SDKs seguem o Python primeiro.
- **Por que rejeitada**: A vantagem de IA pesa mais que a unificação de linguagem.

### Alternativa 2: Java (Spring Boot)

- **Descrição**: Stack corporativa robusta.
- **Prós**: Maturidade, tipagem forte, ferramental amplo.
- **Contras**: Mais verboso; ecossistema de IA/LLM menos idiomático.
- **Por que rejeitada**: Menor velocidade de desenvolvimento no MVP.

## Consequências

### Positivas

- Acesso direto a SDKs oficiais de LLM e ferramentas de NLP.
- FastAPI gera documentação **OpenAPI/Swagger** automaticamente.
- Validação robusta com Pydantic; suporte nativo a `async/await`.

### Negativas

- Desempenho de CPU inferior a Go/Rust (irrelevante para carga _I/O bound_).
- Atenção ao GIL em tarefas CPU-bound.

### Riscos

- Gestão de dependências/ambiente → mitigada por _lockfile_ e imagem de container
  reprodutível ([ADR-0011](0011-docker.md)).

## Notas de Implementação

- Servir com Uvicorn (workers ASGI) atrás de um _reverse proxy_.
- Habilitar a documentação OpenAPI automática do FastAPI.

## Referências

- [arquitetura-c4.md — Seções 5 e 6](../arquitetura-c4.md)
- [ADR-0003 — REST/JSON com OpenAPI](0003-rest-json-openapi.md)
