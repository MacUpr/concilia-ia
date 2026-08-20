# ADR-0012: Explicabilidade e auditoria das decisões de IA

## Status

Aceito

## Data

2026-07-14

## Contexto

Entre os **diferenciais** do produto estão a **explicabilidade da decisão** e a
**padronização**, e a conclusão do projeto destaca **IA responsável**. Além disso,
o MVP entrega um **relatório da decisão**. Para que o conciliador **confie** na
sugestão e para atender a exigências de **transparência e rastreabilidade** (dados
sensíveis de saúde), cada sugestão precisa ser **fundamentada** e cada decisão
precisa ser **auditável**.

## Decisão

Toda sugestão da IA deve vir acompanhada da sua **fundamentação** — as **normas da
ANS** e **cláusulas contratuais** recuperadas (RAG) que a embasam — e ser
registrada numa **trilha de auditoria append-only**. A auditoria guarda: entrada,
contexto recuperado, **sugestão original da IA**, **provedor/modelo** usado e a
**ação do conciliador** (aprovar/ajustar/rejeitar), com autor e carimbo de tempo.

## Alternativas Consideradas

### Alternativa 1: Registrar apenas a decisão final

- **Descrição**: Persistir só o resultado, sem a sugestão original nem o contexto.
- **Prós**: Menos dados armazenados.
- **Contras**: Impossível auditar divergências ou avaliar a qualidade da IA.
- **Por que rejeitada**: Perde rastreabilidade e explicabilidade.

### Alternativa 2: Log de aplicação genérico

- **Descrição**: Depender apenas de logs técnicos.
- **Prós**: Já existe para depuração.
- **Contras**: Não estruturado, volátil, sem garantias de integridade.
- **Por que rejeitada**: Insuficiente como trilha de auditoria de decisões.

## Consequências

### Positivas

- **Confiança** e transparência: a sugestão mostra em que se baseia.
- Base para **métricas de qualidade** (sugestão vs. decisão humana).
- Rastreabilidade completa de quem decidiu o quê e com base em quê.

### Negativas

- Volume de dados de auditoria cresce com o uso.
- Exige cuidado com **dados sensíveis** nos registros.

### Riscos

- Exposição de dados sensíveis na trilha → **minimização**, controle de acesso e
  criptografia; retenção conforme política.

## Notas de Implementação

- Tabela de auditoria **append-only** (sem update/delete); `JSONB` para o contexto.
- Guardar **referências** às normas/cláusulas (IDs), não cópias desnecessárias.
- O relatório da decisão é gerado a partir da auditoria.

## Referências

- [arquitetura-c4.md — Seções 3 e 7](../arquitetura-c4.md)
- [ADR-0007 — pgvector para RAG](0007-pgvector-rag.md)
- [ADR-0009 — Validação humana obrigatória](0009-validacao-humana.md)
