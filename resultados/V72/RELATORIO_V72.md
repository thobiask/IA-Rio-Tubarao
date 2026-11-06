# V72 — Modelos tolerantes a ausência de medições auxiliares

**Data:** 30/10/2026. **Natureza:** experimento exploratório retrospectivo, com base local consolidada; sem aquisição de novas séries horárias.

## Hipótese
É possível aproveitar mais dias para previsão de nível no Rio do Pouso (84580000) sem exigir medições simultâneas de todas as estações auxiliares? Isso melhora a precisão?

## Protocolo
- Fonte: `/mnt/data/base_tratada_ia_com_metadados.csv`, com indicador `nivel_cm_qualidade_estrita=True` e faixa de nível entre -200 e 3000 cm; duplicatas por estação e data excluídas.
- Estação-alvo: 84580000, Rio do Pouso, Tubarão; previsão de nível em D+1 (cm).
- Entradas obrigatórias: níveis do alvo D a D-3 e duas diferenças; entradas auxiliares opcionais: nível D e D-1 das quatro estações de V71 (Pedras Grandes, São Ludgero, Braço do Norte, Orleans-Montante).
- Sem interpolação de medições. Ridge multifonte: imputação pela mediana **aprendida no treino**, indicadores binários de presença de cada entrada auxiliar, padronização e `Ridge(alpha=10)`. HGB multifonte: tratamento nativo de NaN, indicadores de presença, parâmetros fixos.
- Treino até 2015; validação 2016–2020 (não usada para escolher hiperparâmetros); teste 2021–2025 (datas elegíveis observadas até 18/11/2023).
- Comparações de modelos tolerantes a faltantes, Ridge só com alvo e persistência usam **as mesmas 933 datas de teste**. Modelo completo de V71 só pode prever 221 dessas datas; comparar métricas apenas na coorte comum de 221 dias.
- Os dados são diários e o horário de medição/disponibilidade ainda não foi auditado; não são previsões operacionais.

## Cobertura
| Conjunto | Dias com alvo e histórico | Dias com todas as auxiliares |
|---|---:|---:|
| Treino | 6294 | 2953 |
| Validação | 1550 | 557 |
| Teste | 933 | 221 |

A disponibilidade de dias com previsão retrospectiva passou de 221 para 933 (+712, 4,22 vezes), mas apenas quando o histórico recente da estação-alvo está completo.

## Comparação pareada em 933 dias
| Modelo | MAE (cm) | RMSE (cm) |
|---|---:|---:|
| Persistência | **22,147** | 50,550 |
| Ridge só alvo | 23,744 | 48,789 |
| Ridge multifonte tolerante a faltantes | 23,378 | **46,643** |
| HistGradientBoosting multifonte tolerante a faltantes | 22,782 | 49,899 |

**Interpretação:** a persistência mantém menor MAE; Ridge multifonte apresenta menor RMSE, sem prova de superioridade geral.

## Comparação pareada na coorte completa de 221 dias
| Modelo | MAE (cm) |
|---|---:|
| Ridge de casos completos V71 (retreinado) | **21,075** |
| Ridge multifonte tolerante a faltantes | 22,483 |
| Ridge só alvo | 24,927 |
| HistGradientBoosting tolerante a faltantes | 25,410 |
| Persistência | 25,448 |

**Não confundir** o MAE do Ridge V71 nos 221 dias com o MAE dos demais modelos nos 933 dias.

## Subidas >= 50 cm no conjunto de 933 dias (55 eventos observados)
| Modelo | MAE condicionado às 55 subidas (cm) |
|---|---:|
| Ridge multifonte tolerante a faltantes | **132,973** |
| Persistência | 134,236 |
| HistGradientBoosting tolerante a faltantes | 134,746 |
| Ridge só alvo | 136,694 |

O ganho de 1,263 cm frente à persistência é pequeno diante de erros de mais de 130 cm e **não demonstra capacidade de emitir alertas**: o recorte é feito após conhecer a subida real.

## Limitações e próximos testes
1. Verificar fuso horário e disponibilidade efetiva dos dados antes de qualquer uso operacional.
2. Testar indicadores de ausência por estação e padrões de ausência prolongada, com validação cronológica e intervalos de incerteza por blocos temporais.
3. Avaliar modelos de classificação de subida, medindo recall, precisão e falsos alarmes em todas as datas, não apenas nos dias com eventos.
4. Auditar especificamente outubro de 2023: a série elegível termina em novembro de 2023, mas a presença no teste não implica que o episódio esteja integralmente coberto por todas as fontes.
5. Obter dados subdiários oficiais e validar a correspondência das estações.
6. Reavaliar a comparação quando as observações auxiliares forem disponibilizadas de modo assíncrono, com timestamps reais.

**Conclusão:** aceitar ausência de estações auxiliares amplia muito a cobertura retrospectiva, mas ainda não supera a persistência no MAE global. Preservar todas as estações e não implantar sistema de alerta com esses resultados.

## Reproduzir
`python experimento_v72.py` (dependências pandas, numpy, scikit-learn; alterar SOURCE para a localização real da base).
