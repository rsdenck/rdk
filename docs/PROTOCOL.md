# RDK Protocol Specification

## 1. Escopo

Este documento define o contrato do RDK (Ranlens Denck Protocol). Ele descreve apenas o protocolo: tipos de mensagem, envelope, negociacao de versao, operacoes, eventos, erros, autorizacao, idempotencia, ordenacao e compatibilidade.

Implementacoes de agentes, bots, conectores, transportes, persistencia e segredos ficam fora deste repositorio.

As palavras `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` e `MAY` sao normativas.

## 2. Versao

A versao do protocolo e `MAJOR.MINOR.PATCH` conforme `docs/VERSIONING.md`.

Todo envelope `MUST` conter `protocol: "rdk"` e `spec_version`.

Um participante `MUST` rejeitar mensagens com `spec_version` fora da faixa negociada com `RDK_E_UNSUPPORTED_VERSION`.

## 3. Tipos de mensagem

| Tipo | Direcao | Finalidade | Correlacao obrigatoria |
|---|---|---|---|
| `hello` | cliente para servidor |abrir sessao e anunciar versoes | nao |
| `hello_ack` | servidor para cliente |fechar negociacao | `correlation_id` |
| `command` | chamador para executor |solicitar operacao | nao |
| `result` | executor para chamador |retorno de command | `correlation_id` |
| `event` | qualquer participante |fato observavel | nao |
| `error` | qualquer participante |falha de protocolo ou operacao | `correlation_id` quando responder command |

`MUST NOT` existir outro tipo sem bump de major.

## 4. Envelope

Campos obrigatorios para todos os tipos:

| Campo | Tipo | Regra |
|---|---|---|
| `protocol` | string | valor exato `rdk` |
| `spec_version` | string | versao semantica valida |
| `message_id` | string | UUIDv4 unico e imutavel |
| `type` | string | um dos tipos permitidos |
| `sent_at` | string | RFC3339 em UTC |
| `sender` | object | identidade declarada do remetente |
| `target` | object | destinatario ou canal declarado |
| `payload` | object | conteudo especifico do tipo |

Campos opcionais:

| Campo | Tipo | Regra |
|---|---|---|
| `correlation_id` | string | UUIDv4 da mensagem respondida |
| `trace_id` | string | correlacao distribuida |
| `authorization` | object | grant, escopo e expiracao |
| `signature` | object | algoritmo, chave e assinatura |

`message_id` `MUST NOT` ser reutilizado. Reenvio `MUST` preservar `message_id` e usar a mesma idempotency key.

`sent_at` `MUST` usar sufixo `Z`.

## 5. Identidade e autorizacao

`sender` e `target` `MUST` conter ao menos `participant_id` ou `channel`.

`authorization.grant_id` `MUST` ser estavel, nao secreto e auditavel.

`authorization.scope` `MUST` usar o formato `namespace.domain.action` e corresponder a uma operacao registrada.

`authorization.expires_at` `MUST` ser RFC3339 UTC quando presente.

Executor `MUST` validar grant, escopo, expiracao e identificador do chamador antes de produzir efeito externo.

Falta de grant `MUST` resultar em `RDK_E_FORBIDDEN`, nunca em resposta ambígua de sucesso.

## 6. Negociacao de versao

`hello.payload` `MUST` conter:

- `client_id`;
- `supported_versions`;
- `min_supported`;
- `capabilities`.

`hello_ack.payload` `MUST` conter:

- `server_id`;
- `selected_version`;
- `supported_versions`;
- `status`, com valor `accepted` ou `rejected`.

Servidor `MUST` selecionar a maior versao comum.

Se nao houver intersecao, servidor `MUST` responder `hello_ack` com `status: "rejected"` e `RDK_E_UNSUPPORTED_VERSION`.

Depois de `hello_ack` aceito, todas as mensagens da sessao `MUST` usar `selected_version`.

## 7. Commands

`command.payload` `MUST` conter:

- `operation`: identificador registrado em minúsculas;
- `operation_version`: versao semantica da operacao;
- `parameters`: objeto;
- `idempotency_key`: string unica dentro da sessions.

Operacao `MUST` seguir `namespace.domain.action` ou `namespace.action`.

`result.payload` `MUST` conter:

- `operation`;
- `operation_version`;
- `status`: `accepted`, `rejected`, `completed` ou `failed`;
- `data` ou `error`, nunca ambos ao mesmo tempo quando status for terminal.

`accepted` indica que o trabalho foi aceito e ainda nao terminou.

`completed` e `failed` sao estados terminais.

## 8. Events

`event.payload` `MUST` conter:

- `event_type`;
- `event_version`;
- `occurred_at`;
- `subject`;
- `data`.

`event_type` `MUST` seguir `namespace.domain.actioned`, com particípio passado em minúsculas.

`occurred_at` `MUST` ser RFC3339 UTC.

Consumidores `MUST` tratar eventos como no minimo uma vez e deduplicar por `message_id`.

## 9. Erros

`error.payload` `MUST` conter:

- `code`: codigo registrado;
- `message`: texto nao secreto;
- `retryable`: booleano.

Codigos `MUST` pertencer a `registry/error-codes.yaml`.

Codigo removido `MUST NOT` ser reutilizado.

Erros `MUST NOT` conter token, segredo, dado privado ou stack trace.

## 10. Idempotencia e ordenacao

Toda operacao com efeito externo `MUST` exigir `idempotency_key`.

Reexecucao com a mesma chave `MUST` retornar o resultado original ou `RDK_E_IDEMPOTENCY_CONFLICT` se o payload divergir.

Mensagens `SHOULD` ser ordenadas por `sent_at` dentro de um mesmo `channel`, com desempate por `message_id`.

Participantes `MUST` publicar eventos somente apos estado verificavel.

## 11. Seguranca

Mensagens `SHOULD` ser assinadas quando transportadas fora de limite de confiança.

`signature.algorithm` `MUST` ser identificador registrado.

O protocolo nao define algoritmo obrigatorio nesta versao para permitir transportes internos e externos.

Nenhuma implementacao `MUST` aceitar `authorization.grant_id` como prova de posse sem validacao do transporte.

## 12. Conformidade

Uma implementacao e conforme quando:

- valida envelope contra o schema da versao negociada;
- respeita catalogos de operacao e erro;
- preserva `message_id` e `idempotency_key`;
- rejeita versao nao negociada;
- nao inventa tipo, operacao ou codigo de erro fora do catalogo.
