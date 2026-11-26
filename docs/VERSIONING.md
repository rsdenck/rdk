# Padrao de Versionamento RDK

## 1. Fonte de verdade

O arquivo `VERSION` e a unica fonte de verdade da versao do protocolo.

Nenhum outro arquivo pode declarar uma versao diferente da versao de `VERSION` sem ser considerado erro de validacao.

A versao segue `MAJOR.MINOR.PATCH`:

- `MAJOR`: mudanca incompativel de contrato;
- `MINOR`: adicao retrocompativel;
- `PATCH`: correcao sem mudanca de contrato.

Pre-release usa sufixo `-alpha.N`, `-beta.N` ou `-rc.N`.

Build metadata nao e permitido no identificador RDK para evitar ambiguidade de contrato.

## 2. O que cada bump significa

### PATCH

Permitido:

- correcao de typo em documento;
- clarificacao que nao altera validacao;
- novo exemplo de caso ja permitido;
- correcao de link;
- ajuste de mensagem de erro sem troca de codigo.

Proibido:

- novo campo obrigatorio;
- campo antes opcional passar a obrigatorio;
- mudanca de enum;
- mudanca de status;
- mudanca de schema que rejeite mensagem antes aceita.

### MINOR

Permitido:

- novo tipo de mensagem;
- novo campo opcional;
- novo codigo de erro;
- nova operacao;
- nova versao de operacao;
- novo evento;
- novo transporte de referencia;
- ampliacao de escopo sem remover o anterior.

Proibido:

- remover tipo, campo, codigo, operacao ou evento;
- tornar campo opcional em obrigatorio;
- alterar semantica de codigo existente;
- alterar forma de idempotencia.

### MAJOR

Obrigatorio:

- remocao de tipo, campo, codigo, operacao ou evento;
- mudanca de formato de envelope;
- mudanca de semantica que quebre consumidores conformes;
- mudanca de regra de negociacao;
- alteracao de obrigatoriedade;
- reutilizacao de identificador com significado diferente.

Toda major `MUST` publicar tabela de migracao em `docs/COMPATIBILITY.md`.

## 3. Versao por artefato

Todo schema `MUST` publicar `$id` com a familia e a versao major:

`https://github.com/rsdenck/rdk/schema/v1/rdk-envelope.schema.json`

Todo schema `MUST` declarar `$schema` como JSON Schema Draft 2020-12.

Todo exemplo `MUST` declarar `spec_version` igual a `VERSION`.

Toda operacao em `registry/operations.yaml` `MUST` declarar `since`, `status` e `version`.

Todo codigo de erro em `registry/error-codes.yaml` `MUST` declarar `since`, `status`, `retryable` e `description`.

`status` permitido: `active`, `deprecated`, `removed`.

## 4. Versao de operacao

Operacao usa identificador estavel e versao semantica propria:

```json
{
  "operation": "rdk.health.read",
  "operation_version": "1.0.0"
}
```

Regras:

- operacao nova comeca em `1.0.0`;
- adicao retrocompativel em parametros opcionais aumenta minor;
- correcao sem contrato novo aumenta patch;
- mudanca incompativel cria proxima major e mantem a anterior ate deprecacao;
- identificador de operacao removido nunca pode ser reutilizado.

## 5. Versao de evento

Evento usa `event_type` estavel e `event_version` semantica propria.

```json
{
  "event_type": "rdk.session.opened",
  "event_version": "1.0.0"
}
```

Consumidor `MUST` tratar `event_version` como parte do contrato.

Produtor `MUST` manter `event_type` imutavel enquanto a semantica permanecer compativel.

## 6. Negociacao

A versao negociada e sempre a maior versao `MAJOR.MINOR.PATCH` comum entre cliente e servidor.

Participante `MUST NOT` assumir compatibilidade entre majors diferentes sem declaracao explicita em `docs/COMPATIBILITY.md`.

Mensagem recebida com versao maior que a negociada `MUST` ser rejeitada.

Mensagem recebida com versao menor dentro do mesmo major `SHOULD` ser aceita quando o contrato for compativel pelo catalogo.

## 7. Deprecacao

Deprecacao segue tres estados:

1. `active`: uso normal;
2. `deprecated`: ainda funciona, com data alvo de remocao;
3. `removed`: nao aceito, somente em proximo major.

Toda deprecacao `MUST` declarar:

- artefato depreciado;
- versao de deprecacao;
- substituto;
- versao de remocao;
- impacto de migracao.

Nenhum artefato `MUST` ser removido em `patch` ou `minor`.

## 8. Tags e releases

Release `MUST` seguir `v<MAJOR>.<MINOR>.<PATCH>`.

Ordem obrigatoria:

1. branch `release/vX.Y.Z`;
2. atualizacao de `VERSION`;
3. atualizacao de `CHANGELOG.md`;
4. atualizacao de schemas, catalogos e exemplos;
5. `make validate`;
6. merge em `main`;
7. tag assinada;
8. release notes copiadas do changelog.

Tag sem validacao verde e invalida.

## 9. Historico

Changelog e imutavel por versao publicada.

Correcao de changelog de versao publicada `MUST` virar nova entry de patch.

Nenhuma versao publicada pode ser reescrita, re-tagada ou removida.

## 10. Matriz de decisao rapida

| Mudanca | Bump |
|---|---|
| typo sem alterar contrato | patch |
| novo campo opcional | minor |
| novo codigo de erro | minor |
| nova operacao | minor |
| novo evento | minor |
| novo tipo de mensagem | minor |
| campo obrigatorio novo | major |
| remover operacao | major |
| reutilizar codigo de erro | proibido |
| reutilizar id de operacao removida | proibido |
