# Auditoria de cobertura — V69 e V71

Os dados abaixo são derivados dos arquivos originais em `resultados/V69/` e `resultados/V71/`. Não representam nova execução de modelos.

## V69 — cobertura em episódios de interesse

**Chuva diária consolidada, três séries (Orleans, Braço do Norte e Tubarão):**
- Maio de 2022: 16 de 16 dias com valor em cada uma das três séries.
- Outubro de 2023: 0 de 25 dias com valor em cada uma das três séries.

Ausência de valor **não significa precipitação zero**.

**Níveis diários em outubro de 2023 (janela de 25 dias):**
- Orleans Montante (84249998): 0 dias com nível.
- Pedras Grandes (84300000): 12 dias com nível, 0 com nível estrito.
- Braço do Norte (84559800): 25 dias com nível estrito.
- São Ludgero (84560000): 0 dias com nível.
- Rio do Pouso (84580000): 7 dias com nível estrito.

Não há comprovação de medições subdiárias nesses arquivos.

## V71 — comparação de cobertura

| Cenário de disponibilidade | Dias de teste |
|---|---:|
| Todas as estações | 221 |
| Sem Pedras Grandes | 311 |
| Sem São Ludgero | 223 |
| Só alvo | 933 |

Essas coortes têm tamanhos diferentes. Comparar diretamente MAE entre elas não demonstra melhora de modelo. Para comparação de erro entre cenários, consultar o protocolo fixo com 221 dias comuns e `diferencas_bootstrap_v71.csv`.

## Fontes de dados

- `resultados/V69/cobertura_chuva_eventos.csv`
- `resultados/V69/diagnostico_cobertura_eventos.csv`
- `resultados/V69/MANIFESTO.json`
- `resultados/V71/cobertura_v71.csv`
- `resultados/V71/diferencas_bootstrap_v71.csv`

## Limite

Este relatório registra resultados de auditoria retrospectiva; não demonstra aptidão para alerta operacional.
