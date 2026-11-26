RDK Protocol
============

RDK (Ranlens Denck Protocol) e o contrato de comunicacao interna entre participantes autorizados.

Este repositorio contem somente o protocolo RDK: envelope, regras de versao, namespaces, operacoes centrais, eventos, erros, negociacao, seguranca e compatibilidade.

Este repositorio nao contem LEGION AI, agents, bots, conectores, infraestrutura, segredos, tokens, dados privados ou implementacao de transporte especifica.

Versao atual: 1.0.0

Estrutura
---------

- `VERSION`: unica fonte de verdade da versao do protocolo.
- `CHANGELOG.md`: historico publico e imutavel por versao.
- `docs/PROTOCOL.md`: especificacao normativa do protocolo.
- `docs/VERSIONING.md`: padrao completo de versionamento.
- `docs/COMPATIBILITY.md`: matriz de compatibilidade e regras de migracao.
- `docs/GOVERNANCE.md`: governance, release, deprecacao e auditoria.
- `docs/IMPLEMENTATION_GUIDE.md`: guia de conformidade para implementacoes.
- `SECURITY.md`: politica de seguranca e relato privado.
- `CODEOWNERS`: proprietario das revisoes do protocolo.
- `schema/`: JSON Schemas versionados por familia e `index.json`.
- `registry/`: catalogos versionados de operacoes, erros e historico.
- `examples/`: mensagens validas e fixtures invalidas de contrato.
- `tools/validate.py`: validador automatico do repositorio.
- `tools/test_contract.py`: testes automaticos de conformidade do contrato.

Validacao
---------

Requisitos: Python 3.11 ou superior, `jsonschema` e `PyYAML`.

```sh
make validate
```

Regra de ouro
-------------

Nenhuma mudanca de contrato entra em `main` sem versao, changelog, schema, exemplo e validacao automatica.
