# V71 — Seleção de estações: ablação pareada para previsão do Rio do Pouso

**Data:** 30/10/2026. **Natureza:** experimento exploratório local, sem novos dados da ANA.

## Pergunta
A exclusão de estações com cobertura inferior melhora a previsão diária da cota da estação 84580000 (Rio do Pouso, Tubarão)?

## Fonte e protocolo
- Fonte: `base_tratada_ia_com_metadados.csv` (base local ANA consolidada). Estação 84580000 consta erroneamente como Orleans no arquivo de origem; V64 corrigiu documentalmente para Rio do Pouso, Tubarão.
- Alvo: nível do dia seguinte, em centímetros, na estação 84580000. **Não equivale a alerta de enchente**.
- Cinco estações: alvo 84580000; candidatas 84300000 (Pedras Grandes), 84560000 (São Ludgero), 84559800 (Braço do Norte), 84249998 (Orleans-Montante).
- Registros: somente `nivel_cm_qualidade_estrita=True`, valores entre -200 e 3000 cm, datas diárias exatas, sem interpolação. Registros duplicados por código/data excluídos para evitar ambiguidade.
- Entradas do alvo: nível em D, D-1, D-2, D-3 e duas diferenças anteriores; cada estação auxiliar contribui nível em D e D-1. Alvo é D+1.
- Modelo: `StandardScaler` + `Ridge(alpha=10)`; sem otimização no teste. Baseline: persistência (nível D).
- Treino até 2015; validação 2016–2020; teste 2021–2025, respeitando dados elegíveis.
- **Comparação principal de ablação com coorte fixa**: exige disponibilidade das quatro estações auxiliares em D e D-1, mesmo quando excluídas da configuração. Isto preserva exatamente as mesmas datas de treino e teste para todas as variantes. A comparação mede contribuição preditiva, **não** o ganho de cobertura por retirar uma estação.
- Segunda comparação `disponibilidade`: cada variante usa todas as suas datas elegíveis; números **não são comparáveis diretamente** entre configurações devido à mudança de datas e treino.

## Cobertura da coorte fixa
Treino: **2953** dias; validação: **557**; teste: **221**, entre 2021-01-01 e 2023-06-16. A análise **não cobre outubro de 2023**, apesar de o período nominal de teste chegar a 2025.

## Resultados principais: coorte fixa
| Cenário | MAE todos (cm) | MAE subidas ≥50 cm (cm), n=10 | MAE subidas ≥100 cm (cm), n=5 |
|---|---:|---:|---:|
| Todas | 21,075 | 104,272 | 126,240 |
| Sem Pedras Grandes | 21,881 | 100,554 | 121,600 |
| Sem São Ludgero | 23,247 | 98,587 | 120,293 |
| Só Rio do Pouso | 24,848 | 104,586 | 133,871 |
| Persistência | 25,448 | 105,000 | 134,800 |

**Interpretação:** remover Pedras Grandes ou São Ludgero **piora o MAE global** nesta coorte fixa, embora os erros condicionais em dez subidas de ≥50 cm fiquem menores. O tamanho de amostra extremo é insuficiente para afirmar ganho robusto ou eficácia operacional. Não confundir erros em dias com subidas observadas com detecção de eventos em tempo real.

## Disponibilidade quando retiramos estações
- Todas: 221 dias de teste.
- Sem Pedras Grandes: 311 dias de teste.
- Sem São Ludgero: 223 dias de teste.
- Só Rio do Pouso: 933 dias de teste, até 2023-11-18.

Essas amostras diferem; não comparar seus MAEs como se fossem o mesmo conjunto de dias. Excluir estação auxiliar pode recuperar dias utilizáveis, mas também retirar informação preditiva.

## Limitações
1. Estações podem não estar fisicamente conectadas como suposto; metadados e horas reais de leitura não foram revalidados nesta etapa.
2. Apenas Ridge foi retreinado; resultados não demonstram que a exclusão prejudique ou ajude Random Forest, Gradient Boosting ou MLP.
3. Coorte fixa tem somente 221 dias de teste e dez elevações ≥50 cm; o recorte de eventos extremos é frágil.
4. O uso de medições em D pressupõe disponibilidade no instante da previsão; não foi auditado o horário real.
5. A ausência de chuva e a resolução diária continuam limitando a análise.
6. Critério de qualidade estrita não garante ausência de erros hidrológicos; comparar com séries brutas e inventário oficial.
7. Não foram realizadas seleções de variáveis com base no teste para estabelecer um modelo final; cenários são **hipóteses exploratórias**, não decisão definitiva.

## Decisão
**Não excluir definitivamente Pedras Grandes nem São Ludgero.** Manter todas as estações no repositório, mas considerar modelos tolerantes a valores ausentes, máscaras de disponibilidade e comparação em janelas fixas, além de séries horárias. A hipótese de que retirar a pior cobertura aumenta a precisão global **não se confirmou neste teste Ridge**.

## Reproduzir
`python run_v71.py` (ajustar os caminhos de entrada e saída no início do arquivo). Dependências: pandas, numpy, scikit-learn. `finalizar_v71.py` calcula as diferenças e intervalos exploratórios por bootstrap mensal e escreve este relatório.

## Incerteza exploratória das diferenças de MAE (exclusão menos todas)

| cenario              | recorte      |   n |   delta_mae_vs_todas_cm |   ic95_bootstrap_mensal_inf |   ic95_bootstrap_mensal_sup |   reamostragens_validas |
|:---------------------|:-------------|----:|------------------------:|----------------------------:|----------------------------:|------------------------:|
| B_sem_pedras_grandes | todos        | 221 |                   0.806 |                      -0.098 |                       2.214 |                    2000 |
| B_sem_pedras_grandes | subidas_50cm |  10 |                  -3.718 |                      -6.932 |                      -1.964 |                    1997 |
| C_sem_sao_ludgero    | todos        | 221 |                   2.172 |                       1.297 |                       3.025 |                    2000 |
| C_sem_sao_ludgero    | subidas_50cm |  10 |                  -5.685 |                      -6.518 |                      -4.005 |                    1998 |
| D_so_alvo            | todos        | 221 |                   3.773 |                       0.86  |                       8.16  |                    2000 |
| D_so_alvo            | subidas_50cm |  10 |                   0.313 |                      -5.836 |                      13.991 |                    2000 |

Valores negativos favorecem a exclusão. Bootstrap mensal de 2.000 reamostragens, com somente 10 eventos extremos no teste; intervalos são indicativos, não conclusivos.
