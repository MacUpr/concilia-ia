# ADR-0003: Abstração multiprovedor de LLM

## Status

Aceito

## Date

2026-06-29

## Context

O processamento de IA depende de provedores de LLM externos (Anthropic Claude e
OpenAI). Cada provedor tem API, formato de mensagem e modelos próprios. Depender
diretamente de um único provedor cria **_lock-in_**, dificulta _fallback_ em caso
de indisponibilidade e impede escolher o melhor modelo por tarefa/custo.

## Decision

Introduzir um **Gateway de LLM** — uma camada de abstração (padrão _Strategy_/
_Adapter_) com uma interface única (`gerar`, `classificar`) e implementações por
provedor. O domínio (Classificação, Sugestão) **só conhece a interface**, nunca o
SDK concreto. O provedor é selecionável por configuração, com possibilidade de
_fallback_ entre provedores.

## Alternatives Considered

### Alternative 1: Acoplar diretamente a um único provedor (ex.: só OpenAI)

- **Description**: Chamar o SDK do provedor direto nos serviços de domínio.
- **Pros**: Menos código; usa recursos específicos do provedor.
- **Cons**: _Lock-in_; sem _fallback_; troca de provedor exige refatoração ampla.
- **Why rejected**: Risco de dependência de fornecedor e de indisponibilidade.

### Alternative 2: Biblioteca/orquestrador externo (ex.: LangChain, LiteLLM)

- **Description**: Delegar a abstração a um framework de terceiros.
- **Pros**: Pronto para uso, muitos provedores suportados.
- **Cons**: Dependência pesada, _churn_ de API, abstrações genéricas demais.
- **Why rejected**: Interface própria, mínima e controlada, atende o escopo com menos risco. (Reavaliável no futuro.)

## Consequences

### Positive

- Troca de provedor (Anthropic↔OpenAI) sem alterar o domínio.
- _Fallback_ e _A/B_ de modelos por tarefa/custo.
- Testes do domínio com _mock_ do gateway.

### Negative

- Camada adicional para manter.
- A interface tende ao **menor denominador comum** entre as APIs (recursos exclusivos de um provedor ficam de fora ou exigem extensões).

### Risks

- Divergência de comportamento entre provedores (formato/qualidade da saída) →
  mitigado com normalização de saída e testes por provedor.

## Implementation Notes

- Interface: `LLMProvider.gerar(prompt, opcoes) -> Resposta` e `classificar(...)`.
- Implementações: `AnthropicProvider`, `OpenAIProvider`.
- Configuração: provedor primário + ordem de _fallback_ via variável de ambiente.
- Cachear respostas idempotentes no Redis ([ADR-0006](0006-redis-cache-e-fila.md)).

## References

- [arquitetura.md — Seção 5 (Containers)](../arquitetura.md)
