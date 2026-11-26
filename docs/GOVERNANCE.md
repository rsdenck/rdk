# Governance do Protocolo RDK

## 1. Autoridade

O protocolo RDK e propriedade de RANLENS DENCK.

Este repositorio publica somente o contrato do protocolo.

Mudancas de contrato exigem revisao, versao, changelog e validacao automatica.

## 2. Papel dos artefatos

| Artefato | Autoridade |
|---|---|
| `VERSION` | versao canonica do protocolo |
| `docs/PROTOCOL.md` | semantica normativa |
| `docs/VERSIONING.md` | regras de bump e deprecacao |
| `docs/COMPATIBILITY.md` | matriz publica de compatibilidade |
| `schema/*.json` | validacao estrutural e indice de schemas |
| `registry/*.yaml` | catalogos controlados e historico de versoes |
| `examples/*.json` | casos de conformidade validos e invalidos |
| `tools/*.py` | validacao e testes automaticos |
| `SECURITY.md` | politica de seguranca |
| `CODEOWNERS` | revisao obrigatoria |
| `CHANGELOG.md` | historico imutavel |

## 3. Proposta

Toda proposta `MUST` declarar:

- problema;
- impacto de compatibilidade;
- classificacao do bump;
- artefatos alterados;
- plano de migracao quando houver major.

## 4. Revisao

Revisao `MUST` verificar:

- ausencia de codigo fora do protocolo;
- ausencia de segredo ou dado privado;
- versao unica;
- schemas validos;
- exemplos validos;
- catalogos unicos;
- changelog atualizado;
- validacao verde.

## 5. Aprovacao

Aprovacao e registrada por commit assinado e tag assinada.

Nenhuma mudanca de contrato entra em producao sem tag `vX.Y.Z`.

## 6. Auditoria

Cada release `MUST` manter:

- tag assinada;
- entry de changelog;
- logs de CI;
- diff revisado;
- matriz de compatibilidade atualizada.

## 7. Segredo

Nenhum arquivo deste repositorio pode conter token, senha, chave privada, URL de webhook, CPF, endereco, e-mail pessoal ou qualquer dado privado.

Violacao disto e bloqueio imediato de release e requer rotacao fora deste repositorio.

## 8. Fora do escopo

Nao pertencem a este repositorio:

- implementacao de agents ou bots;
- conectores externos;
- persistencia;
- infraestrutura;
- prompts;
- memoria operacional;
- ordens financeiras;
- dados de carteira;
- credenciais;
- logs reais de producao.
