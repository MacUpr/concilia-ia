# ADR-0009: Proteção de dados de saúde e LGPD

## Status

Aceito

## Date

2026-06-29

## Context

O sistema processa **dados pessoais sensíveis de saúde** (LGPD, Lei nº 13.709/2018,
art. 11). Há ainda o envio de conteúdo das reclamações a **provedores de LLM
externos**, o que exige cuidado com exposição de dados a terceiros. A natureza
jurídica do processo torna **rastreabilidade** e **proteção** requisitos de
primeira ordem.

## Decision

Adotar um conjunto de controles de privacidade e segurança como requisito
arquitetural:

1. **Criptografia** em trânsito (TLS) e em repouso (dados sensíveis no PostgreSQL).
2. **Controle de acesso** por papel (cliente vs. conciliador) e autorização nos endpoints.
3. **Minimização de dados** enviados ao LLM (anonimização/pseudonimização e remoção
   de identificadores diretos sempre que possível).
4. **Gestão de segredos** (chaves de API de LLM fora do código, em cofre/variáveis seguras).
5. **Trilha de auditoria** append-only de decisões e acessos
   ([ADR-0005](0005-postgresql-persistencia-e-auditoria.md)).

## Alternatives Considered

### Alternative 1: Tratar segurança só na borda (TLS) e nada além

- **Description**: Confiar apenas no TLS e na rede.
- **Pros**: Simples.
- **Cons**: Não cobre dados em repouso, acesso indevido, nem exposição ao LLM.
- **Why rejected**: Insuficiente para dados sensíveis de saúde.

### Alternative 2: Não enviar dados a LLM externo (somente modelo local)

- **Description**: Hospedar um modelo próprio para nunca expor dados a terceiros.
- **Pros**: Máxima proteção contra exposição externa.
- **Cons**: Custo/infra altos; qualidade inferior aos LLMs gerenciados nesta fase.
- **Why rejected**: Inviável agora; mitigamos com minimização/anonimização e cláusulas de não-treinamento.

## Consequences

### Positive

- Conformidade com LGPD; redução de risco de vazamento.
- Rastreabilidade completa de decisões e acessos.

### Negative

- Anonimização pode reduzir o contexto disponível à IA (trade-off qualidade × privacidade).
- Mais complexidade (gestão de chaves, criptografia, RBAC).

### Risks

- Exposição de dados ao provedor de LLM → mitigado com minimização, contratos/DPAs
  e provedores que **não treinam** com os dados enviados.
- Vazamento de segredos → mitigado com cofre de segredos e rotação de chaves.

## Implementation Notes

- TLS obrigatório; criptografia de colunas sensíveis.
- Camada de **redação/anonimização** antes de chamar o Gateway de LLM.
- RBAC nos endpoints; _logs_ sem dados sensíveis em texto puro.

## References

- LGPD — Lei nº 13.709/2018 (art. 11, dados sensíveis de saúde)
- [ADR-0004 — Validação humana obrigatória](0004-validacao-humana-obrigatoria.md)
- [ADR-0003 — Abstração multiprovedor de LLM](0003-abstracao-multiprovedor-llm.md)
