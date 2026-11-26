# Changelog

Todas as mudancas relevantes deste protocolo sao documentadas aqui.

O formato segue `MAJOR.MINOR.PATCH` e a definicao em `docs/VERSIONING.md`.

## [1.0.0] - 2026-11-25

### Added

- Envelope canonico RDK com `hello`, `hello_ack`, `command`, `result`, `event` e `error`.
- Negociacao de versao com `supported_versions`, versao selecionada e falha explicita quando nao ha intersecao.
- Padrao de versionamento semantico do protocolo, de operacoes, de eventos e de catalogos.
- Matriz de compatibilidade e regras de deprecacao.
- JSON Schemas para todas as familias de mensagem.
- Catalogos versionados de operacoes centrais e codigos de erro.
- Exemplos executaveis de cada familia de mensagem.
- Fixtures invalidas para garantir rejeicao de versao e status fora do contrato.
- Indice de schemas e historico de versoes legivel por maquina.
- Guia de implementacao conforme, politica de seguranca e CODEOWNERS.
- Validador automatico de versao, schemas, exemplos, catalogos e regra de fala.
- Testes automaticos de conformidade, incluindo ausencia de emoji e U+2014.

### Security

- Exigencia de identificador de mensagem, correlacao e autorizacao declaraveis.
- Regra de nao reutilizacao de codigos de erro e de nao remocao de operacao sem bump de major.
