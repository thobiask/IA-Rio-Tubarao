# Auditoria das previsões individuais V73

Fonte analisada: arquivo local original `resultados/V73/previsoes_v73.csv`, com **11.196 linhas** (12 configurações × 933 datas), entre 2021-01-01 e 2023-11-18.

SHA-256 do original: `aba1e7e637a633e9e8e4be7ce63eff44bfcfcea5a2f5184a400b3163853ed720`.

A tabela `matriz_confusao_recalculada.csv` foi **calculada novamente** a partir de `observado_evento` e `alerta` no arquivo original. Não é uma cópia de métricas reportadas anteriormente.

## Resultados relevantes

| Subida | Modelo e regra | TP | FP | FN | Precisão | Recall |
|---|---|---:|---:|---:|---:|---:|
| ≥50 cm | Regressão logística, ajustado na validação | 35 | 451 | 20 | 7,2% | 63,6% |
| ≥50 cm | HGB, ajustado na validação | 27 | 217 | 28 | 11,1% | 49,1% |
| ≥50 cm | Regressão logística, limiar fixo 0,50 | 19 | 131 | 36 | 12,7% | 34,5% |
| ≥100 cm | Regressão logística, ajustado na validação | 3 | 50 | 23 | 5,7% | 11,5% |
| ≥100 cm | HGB, ajustado na validação | 3 | 39 | 23 | 7,1% | 11,5% |

São **55** subidas observadas ≥50 cm e **26** ≥100 cm no conjunto de 933 datas. Nenhum desses resultados demonstra capacidade operacional de alerta.

## Controle de qualidade do arquivo de origem

- 11.196 registros, 9 colunas e 12 configurações com exatamente 933 registros cada.
- Nenhuma duplicata de `data_emissao`, `limiar_subida_cm`, `modelo` e `regra`.
- Nenhum nulo em `data_emissao`, `data_alvo`, `limiar_subida_cm`, `modelo`, `regra`, `observado_evento`, `alerta` ou `subida_real_cm`.
- **3.732 probabilidades ausentes**: pertencem às regras basais, que não produzem probabilidades; não devem ser imputadas artificialmente.
- Este diagnóstico **não verifica** se os dados estavam disponíveis no momento da previsão.

## Pendência de publicação

O arquivo completo `previsoes_v73.csv` (829.326 bytes) ainda não foi enviado ao GitHub. Foi preservado em um pacote de pendências para importação via GitHub Desktop. A tabela de matrizes recalculadas já está publicada.

**Cuidado metodológico:** um falso positivo é um dia classificado como subida que não atingiu o limiar escolhido. Não é necessariamente um falso aviso de inundação, pois a variável prevista é subida diária, não dano ou transbordamento validado.
