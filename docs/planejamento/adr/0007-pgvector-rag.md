# ADR-0007: pgvector para busca semântica das normas da ANS (RAG)

## Status

Aceito

## Data

2026-07-14

## Contexto

Uma capacidade central do MVP é a **consulta das normas da ANS** e o uso da IA
para **fundamentar as sugestões** nas normas e nos contratos das operadoras. Para
fornecer contexto relevante ao LLM (padrão **RAG — _Retrieval-Augmented
Generation_**) e **reduzir alucinação**, é preciso recuperar trechos de normas e
cláusulas **semanticamente** relacionados a cada pedido — não apenas por
correspondência de palavras. Isso exige **busca por similaridade** sobre
**embeddings vetoriais**. O sistema já usa PostgreSQL ([ADR-0005](0005-postgresql-sqlalchemy.md)).

## Decisão

Usar a extensão **pgvector** no PostgreSQL para armazenar **embeddings** de normas
da ANS e cláusulas contratuais, e realizar **busca por similaridade** (distância
de cosseno / produto interno) para montar o contexto do RAG. Tudo permanece no
**mesmo banco relacional**, sem introduzir um _vector database_ dedicado nesta
fase.

## Alternativas Consideradas

### Alternativa 1: Vector database dedicado (Pinecone, Weaviate, Qdrant)

- **Descrição**: Serviço especializado em busca de vetores.
- **Prós**: Otimizado para escala massiva de vetores.
- **Contras**: Mais um sistema para operar e custear; sincronização com o relacional.
- **Por que rejeitada**: O volume do MVP não justifica; pgvector reaproveita o PostgreSQL.

### Alternativa 2: Busca textual (full-text / BM25)

- **Descrição**: Recuperação por índice textual e ranqueamento léxico.
- **Prós**: Simples; não depende de embeddings.
- **Contras**: Não captura similaridade **semântica**; recall pior para linguagem jurídica.
- **Por que rejeitada**: Qualidade do RAG inferior para o domínio.

## Consequências

### Positivas

- **Um único banco** — dados relacionais e vetores juntos, com ACID.
- Índices ANN (HNSW / IVFFlat) para busca eficiente.
- Base para **explicabilidade**: a sugestão cita as normas recuperadas.

### Negativas

- Escala de vetores menor que soluções dedicadas.
- Depende de um modelo/serviço externo para gerar embeddings.

### Riscos

- Custo/latência da geração de embeddings → _cache_ de embeddings.
- Troca do modelo de embedding altera o espaço vetorial → exige **re-indexação** e
  **versionamento**.

## Notas de Implementação

- Coluna do tipo `vector`; índice **HNSW**.
- _Pipeline_ de ingestão das normas da ANS (extração → _chunking_ → embedding →
  indexação).
- Embeddings gerados via **gateway multiprovedor** ([ADR-0008](0008-llm-multiprovedor.md)).

## Referências

- [arquitetura-c4.md — Seções 6 e 7](../arquitetura-c4.md)
- [ADR-0005 — PostgreSQL + SQLAlchemy](0005-postgresql-sqlalchemy.md)
- [ADR-0008 — LLM multiprovedor](0008-llm-multiprovedor.md)
