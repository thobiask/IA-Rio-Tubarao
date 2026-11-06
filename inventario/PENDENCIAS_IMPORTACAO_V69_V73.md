# Estado de importação das previsões V69–V73

**Conferência em 06/11/2026:** os cinco arquivos abaixo não constavam na comparação entre `main` e `revisao-inicial`. Os arquivos estão disponíveis no pacote `IA_Rio_Tubarao_pendentes_para_GitHub.zip` desta conversa.

| Arquivo | Bytes originais | Situação |
|---|---:|---|
| `experimentos/V69/reproduzir_v69.py` | 8455 | Pendente |
| `resultados/V69/RELATORIO_V69.md` | 6022 | Pendente |
| `resultados/V71/previsoes_pareadas_v71.csv` | 62370 | Pendente |
| `resultados/V72/previsoes_v72.csv` | 292653 | Pendente |
| `resultados/V73/previsoes_v73.csv` | 829326 | Pendente |

## Procedimento de importação
1. No GitHub Desktop, conferir `Current branch: revisao-inicial` e clicar em `Fetch origin`.
2. Abrir `Repository > Show in Explorer`.
3. Extrair o **conteúdo interno** do ZIP diretamente na raiz da pasta `IA-Rio-Tubarao`, preservando `experimentos/` e `resultados/`. **Não** criar uma pasta adicional com o nome do ZIP.
4. Conferir cinco arquivos novos na lista `Changes`. Se houver substituições ou conflitos, interromper e revisar antes de confirmar.
5. Criar commit `dados: completar scripts e previsoes historicas V69-V73` e clicar `Push origin`.
6. Verificar no GitHub que os cinco caminhos acima estão acessíveis na branch de revisão.

## Limites da auditoria
A publicação dos arquivos não comprova reprodutibilidade, disponibilidade dos dados no momento de previsão ou eficácia operacional. É necessário verificar integridade (hashes), executar scripts com ambiente registrado e auditar os eventos críticos.
