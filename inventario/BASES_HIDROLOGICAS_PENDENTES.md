# Inventário das oito bases hidrológicas locais

**Situação em 30/10/2026:** arquivos presentes no pacote local, mas **NÃO enviados ao GitHub**. Este manifesto registra os arquivos que precisam ser transferidos. O fato de constarem aqui não significa que estejam publicados.

| Caminho relativo | Tamanho (bytes) | Linhas de dados* | SHA-256 |
|---|---:|---:|---|
| `dados/chuva/chuva_tubarao_02849027_acumulados.csv` | 1757082 | 14335 | `9ca549c7108fed36bcc810c8f84a8208bd1de9504f4e5ba1fe0a15725c3b5223` |
| `dados/chuva/chuvas_orleans_braco_norte_tubarao_24h_48h_72h.csv` | 3195046 | 31716 | `c6c913715ff3c50cb9f132799cd55db258f07a028b48c2aff22f04dde58119b6` |
| `dados/chuva/modelo_acumulados_chuva_1939_2026.csv` | 5155767 | 140103 | `0c0f4957e4976d7ddd9d8af6e6d97a8e517502a5bfc8332b8b119df445057751` |
| `dados/processados/base_ia_hidrologia_chuvas_3_estacoes.csv` | 47230545 | 140103 | `89d8c4a7a930eef922b71825384fefbf19d0c923a5c9c249bb147f36600be0e8` |
| `dados/processados/base_tratada_ia_com_metadados.csv` | 48577856 | 140103 | `af74cec95a5029484f4edf3a421faa1a681bf2fcb93986d20e428e0482b24bb7` |
| `dados/processados/base_tratada_ia_rios_chuvas_alunos.csv` | 19099594 | 140103 | `990ef62d589b2e647c4dee7108e15c281753720984f5370d6fbdd21b10e75445` |
| `dados/processados/dados_hidrologicos_com_chuva_tubarao.csv` | 53961586 | 140103 | `b46c798761c7ea3fc38e3aa6cf72c193186276403e47ba9c272452edeb4f1ffd` |
| `dados/processados/dados_hidrologicos_ia.csv` | 30165942 | 140103 | `7895a93a7be7ece9598b5197e8adf27afa555ef38aa27471df487b588e2cced9` |

*Linhas contadas por quebra de linha menos o cabeçalho. O total de linhas não equivale a quantidade de observações válidas.

## Conteúdo identificado
As bases processadas incluem campos como `data`, `estacao_codigo`, `nivel_cm`, `nivel_m`, `vazao_m3_s`, indicadores de qualidade, e, conforme o arquivo, chuva diária e acumulada de 24/48/72 horas.

## Próxima ação
Transferir os oito arquivos, preservando os nomes e caminhos. Depois conferir os SHA-256 da versão recebida e auditar a origem e os termos de redistribuição. Nenhum dado bruto novo foi coletado nesta etapa.

**Importante:** repositório privado não substitui auditoria de licenças, qualidade e disponibilidade temporal das medições.
