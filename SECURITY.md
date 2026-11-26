# Seguranca

Este repositorio publica somente o contrato publico do protocolo RDK.

Nao envie para este repositorio:

- tokens, senhas, chaves privadas ou certificados;
- credenciais de qualquer plataforma;
- dados pessoais ou privados;
- logs de producao com identificadores reais;
- payloads que exponham segredos de negocio;
- informacao operacional nao autorizada.

Vulnerabilidades ou problemas de seguranca devem ser reportados privadamente ao mantenedor do repositorio.

O relato deve conter:

- artefato afetado;
- impacto;
- passos para reproduzir sem dados reais;
- versao afetada;
- sugestao de correcao quando disponivel.

Nenhum relato deve ser publicado em issue antes da correcao.

A resposta de seguranca segue a ordem:

1. confirmar recebimento;
2. classificar impacto;
3. corrigir em branch privada;
4. publicar patch ou minor conforme `docs/VERSIONING.md`;
5. registrar entrada em `CHANGELOG.md` sem detalhes exploraveis.

Codigos de erro e mensagens normativas nunca podem revelar segredo, chave, endereco privado ou dado pessoal.
