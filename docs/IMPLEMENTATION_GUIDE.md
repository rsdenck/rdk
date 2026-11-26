# Guia de Implementacao Conforme

Este guia descreve como uma implementacao deve consumir o contrato RDK sem alterar o protocolo.

## 1. Carregamento do contrato

A implementacao deve carregar:

1. `VERSION`;
2. `docs/PROTOCOL.md`;
3. `docs/VERSIONING.md`;
4. `docs/COMPATIBILITY.md`;
5. `schema/index.json`;
6. `registry/operations.yaml`;
7. `registry/error-codes.yaml`.

Nenhuma implementacao deve inventar tipo de mensagem, operacao, evento ou codigo de erro.

## 2. Validacao de entrada

Toda mensagem recebida deve ser validada nesta ordem:

1. UTF-8 valido;
2. JSON object valido;
3. envelope da versao negociada;
4. schema especifico do tipo;
5. versao declarada igual a versao negociada;
6. operacao ou evento presente no catalogo;
7. autorizacao, escopo e expiracao;
8. idempotencia quando aplicavel.

Falha em qualquer etapa deve interromper o processamento.

## 3. Negociacao

A sessao so comeca apos `hello_ack` com `status: "accepted"`.

A versao selecionada deve ser a maior versao comum.

Depois da negociacao, toda mensagem deve usar exatamente `selected_version`.

## 4. Commands

Executor deve registrar:

- `message_id` do command;
- `idempotency_key`;
- `operation`;
- `operation_version`;
- estado `accepted`, `rejected`, `completed` ou `failed`;
- `correlation_id` do resultado.

Resultado terminal nao pode conter simultaneamente `data` e `error`.

## 5. Eventos

Consumidor deve deduplicar por `message_id`.

Produtor nao pode reemitir o mesmo evento com `message_id` diferente para representar o mesmo fato.

`event_version` faz parte do contrato do evento.

## 6. Erros

Mensagem de erro deve usar codigo registrado.

Mensagem livre deve ser segura para exibicao e nao conter segredo.

Codigo nao registrado deve ser tratado internamente como erro de implementacao, nunca promovido a codigo oficial.

## 7. Conformidade de repositorio

Antes de publicar uma versao:

1. `make validate`;
2. revisar `CHANGELOG.md`;
3. revisar `docs/COMPATIBILITY.md`;
4. confirmar que nao ha arquivo fora do escopo do protocolo;
5. confirmar que nao ha emoji ou caractere U+2014.
