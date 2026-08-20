# ADR-0004: Autenticação e autorização via JWT

## Status

Aceito

## Data

2026-07-14

## Contexto

A API expõe endpoints (`/login`, `/solicitacoes`, `/upload`, `/analise`,
`/resultado`) consumidos por uma Aplicação Web. É preciso **autenticar** os
usuários (conciliadores, servidores, administradores) e **autorizar** o acesso a
**dados sensíveis de saúde**. A API deve permanecer **stateless** para escalar
horizontalmente.

## Decisão

Adotar autenticação baseada em **tokens JWT** assinados. O endpoint `POST /login`
valida as credenciais e emite um **access token** (curta duração) e um **refresh
token**. Os tokens carregam _claims_ de identidade e **papel** (RBAC:
`conciliador`, `servidor`, `administrador`). Os endpoints protegidos validam a
assinatura e os _claims_ via dependência do FastAPI. Sem estado de sessão no
servidor.

## Alternativas Consideradas

### Alternativa 1: Sessão server-side com cookie

- **Descrição**: Sessão mantida no servidor, referenciada por cookie.
- **Prós**: Revogação imediata; modelo simples.
- **Contras**: Introduz estado no servidor; atrito com _statelessness_.
- **Por que rejeitada**: Contraria a API _stateless_ replicável ([ADR-0001](0001-api-rest-unica.md)).

### Alternativa 2: OAuth2/OIDC com IdP federado (ex.: Keycloak)

- **Descrição**: Delegar autenticação a um _Identity Provider_.
- **Prós**: SSO e gestão robusta de identidade.
- **Contras**: Infraestrutura adicional fora do escopo do MVP.
- **Por que rejeitada**: _Overkill_ para o MVP; fica como evolução.

## Consequências

### Positivas

- Autenticação _stateless_ → escala horizontal sem afinidade de sessão.
- Padrão amplamente suportado; RBAC diretamente nos _claims_.

### Negativas

- Revogação antes da expiração exige _blocklist_.
- O cliente precisa proteger os tokens.

### Riscos

- Vazamento de token → mitigado por **HTTPS**, **curta expiração**, **rotação** do
  refresh e **segredo forte** de assinatura.

## Notas de Implementação

- `OAuth2PasswordBearer` do FastAPI; assinatura HS256 (ou RS256).
- Access token ~15 min + refresh token de vida mais longa.
- Senhas com _hash_ forte (bcrypt/argon2), nunca em texto claro.

## Referências

- [arquitetura-c4.md — Seção 6](../arquitetura-c4.md)
- [ADR-0003 — REST/JSON com OpenAPI](0003-rest-json-openapi.md)
- [ADR-0012 — Explicabilidade e auditoria](0012-explicabilidade-auditoria.md)
