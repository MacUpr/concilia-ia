# ADR-0010: Armazenamento de documentos e contratos (upload)

## Status

Aceito

## Data

2026-07-14

## Contexto

Funcionalidades do MVP incluem **upload do contrato** e **upload dos documentos**
(`POST /upload`). Esses arquivos são **binários** (PDF, imagens), podem ser
**grandes**, contêm **dados sensíveis de saúde** e alimentam a análise de IA (texto
extraído para o RAG). É preciso decidir **onde** e **como** armazená-los.

## Decisão

Armazenar os **arquivos binários em object storage** compatível com **S3** (ex.:
MinIO em desenvolvimento/on-prem, bucket gerenciado em produção), guardando no
PostgreSQL apenas os **metadados e referências** (chave do objeto, tipo, _hash_,
tamanho, vínculo com a solicitação). O texto extraído para o RAG é processado e
indexado via pgvector ([ADR-0007](0007-pgvector-rag.md)).

## Alternativas Consideradas

### Alternativa 1: Guardar binários no PostgreSQL (BYTEA / Large Objects)

- **Descrição**: Persistir os arquivos dentro do banco.
- **Prós**: Um só sistema; transacional.
- **Contras**: Incha o banco; prejudica _backup_, replicação e desempenho.
- **Por que rejeitada**: Não escala para binários grandes.

### Alternativa 2: Sistema de arquivos local do container

- **Descrição**: Salvar no disco do container da API.
- **Prós**: Simples.
- **Contras**: Efêmero, não compartilhado entre réplicas, não durável.
- **Por que rejeitada**: Contraria a API _stateless_/replicável ([ADR-0001](0001-api-rest-unica.md)).

## Consequências

### Positivas

- Banco enxuto e rápido; _storage_ escalável e durável.
- **URLs pré-assinadas** para acesso controlado; separação metadados × binário.

### Negativas

- Mais um serviço (object storage) para operar.
- Consistência eventual entre metadado e objeto.

### Riscos

- Acesso indevido a dados sensíveis → **criptografia em repouso**, **URLs de curta
  duração** e controle de acesso.
- Órfãos (objeto sem metadado ou vice-versa) → rotina de **reconciliação**.

## Notas de Implementação

- Cliente S3 (boto3/aioboto3); validação de **tipo e tamanho** no upload.
- Chave por solicitação; criptografia SSE; retenção conforme sensibilidade do dado.
- _Scan_ antivírus opcional antes de processar.

## Referências

- [arquitetura-c4.md — Seções 5 e 7](../arquitetura-c4.md)
- [ADR-0007 — pgvector para RAG](0007-pgvector-rag.md)
- [ADR-0012 — Explicabilidade e auditoria](0012-explicabilidade-auditoria.md)
