# ADR-0001: Arquitetura como única API REST (mono-serviço)

## Status

Aceito

## Data

2026-07-14

## Contexto

O MVP precisa **receber a solicitação, interpretar o pedido, consultar normas e
contratos, aplicar IA e sugerir a estratégia de conciliação**. É um time pequeno,
com prazo de poucas _sprints_ e escopo bem delimitado (cadastros, upload, consulta
ANS, análise de IA, sugestão e relatório).

É preciso definir a **granularidade** da arquitetura: um único serviço ou vários
serviços independentes (microsserviços).

## Decisão

Construir a solução como uma **única API REST** (mono-serviço), organizada
internamente em módulos/componentes coesos (autenticação, cadastros, solicitações,
upload, motor de análise). Todo o processamento — inclusive a orquestração da IA —
fica concentrado nesse serviço.

## Alternativas Consideradas

### Alternativa 1: Microsserviços

- **Descrição**: Separar autenticação, análise de IA, cadastros etc. em serviços
  independentes.
- **Prós**: Escala e _deploy_ independentes; isolamento de falhas.
- **Contras**: _Overhead_ operacional (rede, observabilidade, orquestração)
  elevado para o tamanho do time e do MVP.
- **Por que rejeitada**: Complexidade injustificada nesta fase.

### Alternativa 2: Funções serverless

- **Descrição**: Cada endpoint como função gerenciada.
- **Prós**: Escala automática; custo por uso.
- **Contras**: _Cold start_, limites de execução para chamadas longas de LLM,
  fragmentação da lógica.
- **Por que rejeitada**: Ruim para orquestração de IA com estado e chamadas longas.

## Consequências

### Positivas

- Simplicidade operacional: um _deploy_, um _pipeline_, um ponto de observação.
- Menor latência interna (chamadas em processo, sem rede entre módulos).
- Evolução rápida no ritmo do MVP.

### Negativas

- Acoplamento interno maior que em microsserviços.
- Todo o serviço escala junto (mesmo que só a análise seja pesada).

### Riscos

- Crescimento do escopo tornar o mono-serviço grande → mitigado por **fronteiras
  de módulo bem definidas** que permitem extrair serviços no futuro.

## Notas de Implementação

- Organizar por módulos com contratos internos claros (facilita extração futura).
- Manter a API **stateless** para permitir réplicas horizontais.

## Referências

- [arquitetura-c4.md — Seções 5 e 6](../arquitetura-c4.md)
