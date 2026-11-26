# Compatibilidade RDK

## Matriz de compatibilidade

| Versao do protocolo | Status | Compativel com | Observacao |
|---|---|---|---|
| `1.0.0` | active | `1.x` | contrato inicial estavel |

## Regras de compatibilidade

1. Mensagens `1.x` nao podem ser rejeitadas por implementacao `1.y` quando validas contra o mesmo major e quando nao usarem artefato depreciado removido.
2. Implementacao `1.x` deve aceitar campo opcional desconhecido somente quando o schema permitir; caso contrario deve rejeitar com `RDK_E_INVALID_ENVELOPE`.
3. Valor de enumeracao desconhecido deve ser rejeitado, nunca interpretado.
4. Codigo de erro desconhecido deve ser tratado como `RDK_E_INTERNAL` sem alterar o codigo original nos logs.
5. Operacao desconhecida deve ser rejeitada com `RDK_E_NOT_FOUND`.
6. Versao principal diferente nao e compativel por padrao.

## Migracao

Tabela de migracao por major:

| De | Para | Acao obrigatoria |
|---|---|---|
| nenhuma | `1.0.0` | adotar envelope, negociacao, catalogos e validacao |

## Remocoes planejadas

Nenhuma.

## Politica de convivencia de versoes

Servidor pode aceitar multiplos majors simultaneamente desde que:

- a negociacao escolha explicitamente um major;
- cada mensagem carregue `spec_version` coherente;
- catalogos por major sejam mantidos em diretorio separado;
- a tabela acima documente o periodo de convivencia.

## Incompatibilidades conhecidas

Nenhuma.
