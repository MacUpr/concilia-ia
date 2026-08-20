# ADR-0008: Integração multiprovedor de LLM (OpenAI/Claude)

## Status

Aceito

## Data

2026-07-14

## Contexto

A análise inteligente do pedido e a geração da sugestão dependem de um **LLM**. O
PDF cita **OpenAI/Claude** como opções. LLMs são serviços **externos**, com
**latência, custo e disponibilidade variáveis**, e evoluem rápido (novos modelos,
mudança de preços). Depender de um único provedor cria **risco de _lock-in_** e de
indisponibilidade.

## Decisão

Isolar o acesso ao LLM atrás de um **Gateway de LLM** (camada de abstração), com
uma interface única e **adaptadores por provedor** (OpenAI e Anthropic Claude). A
seleção do provedor/modelo é **configurável**, permitindo _fallback_ entre
provedores.

## Alternativas Consideradas

### Alternativa 1: Integração direta com um único provedor

- **Descrição**: Chamar o SDK de um provedor diretamente na lógica de negócio.
- **Prós**: Mais simples e rápido de implementar.
- **Contras**: _Lock-in_; troca de provedor exige mudar código espalhado.
- **Por que rejeitada**: Falta de portabilidade e resiliência.

### Alternativa 2: Framework de orquestração pesado

- **Descrição**: Adotar um framework amplo de _orchestration_ de LLM.
- **Prós**: Muitos recursos prontos.
- **Contras**: Complexidade e dependência grandes para a necessidade do MVP.
- **Por que rejeitada**: _Overkill_; uma abstração fina é suficiente.

## Consequências

### Positivas

- Evita _lock-in_; troca de provedor/modelo por configuração.
- **Resiliência**: _fallback_ entre provedores em caso de falha.
- Ponto único para _timeouts_, _retry_, _cache_ e controle de custo.

### Negativas

- Camada extra de abstração para manter.
- Recursos ficam limitados ao **menor denominador comum** entre as APIs.

### Riscos

- Diferença de comportamento entre provedores → mitigada por testes e _prompts_
  parametrizados por adaptador.

## Notas de Implementação

- Interface `LLMProvider` com implementações `OpenAIProvider` e `ClaudeProvider`.
- _Timeouts_, _retry_ com _backoff_ e _fallback_ configuráveis.
- Segredos de API protegidos (variáveis de ambiente / cofre de segredos).
- O Gateway também gera **embeddings** para o RAG ([ADR-0007](0007-pgvector-rag.md)).

## Referências

- [arquitetura-c4.md — Seção 6](../arquitetura-c4.md)
- [ADR-0009 — Validação humana obrigatória](0009-validacao-humana.md)
