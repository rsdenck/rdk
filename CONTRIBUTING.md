# Contribuicao

Toda contribuicao deve alterar somente o protocolo RDK.

Antes de abrir uma mudanca:

1. Leia `docs/PROTOCOL.md`, `docs/VERSIONING.md` e `docs/COMPATIBILITY.md`.
2. Declare o impacto da mudanca: `patch`, `minor` ou `major`.
3. Atualize `VERSION`, `CHANGELOG.md`, `schema/index.json`, `registry/version-history.yaml`, schemas, catalogos e exemplos no mesmo commit.
4. Execute `make validate`.
5. Descreva a compatibilidade na mensagem do commit e no pull request.

Sao proibidos:

- codigo de agent, bot, conector ou infraestrutura;
- token, segredo, credencial ou dado privado;
- mudanca silenciosa de contrato;
- reutilizacao de codigo de erro;
- remocao de operacao sem deprecacao documentada e bump de major;
- uso do caractere U+2014 em qualquer arquivo.

Branches: `main`, `feat/<slug>`, `fix/<slug>`, `docs/<slug>` e `release/v<major>.<minor>.<patch>`.

Tags de release: `v<major>.<minor>.<patch>`.
