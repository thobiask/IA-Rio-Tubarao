# Auditoria comparativa V71–V73 — limites de interpretação

**Estado:** análise documental dos resultados históricos publicados; não constitui reexecução dos modelos.

## V71 — efeito de retirar estações

Na coorte fixa de **221 dias**:
- Ridge com todas as estações: MAE **21,075 cm**.
- Sem Pedras Grandes: **21,881 cm**.
- Sem São Ludgero: **23,247 cm**.
- Somente a estação-alvo: **24,848 cm**.
- Persistência: **25,448 cm**.

A exclusão de estações piora o MAE global nessa coorte. As comparações de disponibilidade usam coortes distintas (221, 311, 223 e 933 dias) e não podem fundamentar ranking direto entre modelos.

## V72 — tratamento de medições auxiliares ausentes

Na coorte de **933 dias**:
| Modelo | MAE (cm) | RMSE (cm) |
|---|---:|---:|
| Persistência | **22,147** | 50,550 |
| Ridge só alvo | 23,744 | 48,789 |
| Ridge multifonte tolerante a ausências | 23,378 | **46,643** |
| HGB multifonte tolerante a ausências | 22,782 | 49,899 |

O Ridge multifonte reduz RMSE frente à persistência, mas **não reduz MAE**. Em **55 dias com subida observada ≥50 cm**, o MAE do Ridge multifonte ainda é **132,973 cm** (persistência: 134,236 cm). Os recortes são retrospectivos e não demonstram capacidade de alerta antecipado.

## V73 — classificação de subida

Conforme os resultados históricos da V73, o teste tem **933 dias**, com **55 subidas ≥50 cm** e **26 subidas ≥100 cm**. Um exemplo de limiar da regressão logística (0,35) registra **35 verdadeiros positivos, 451 falsos positivos e 20 falsos negativos** para subidas ≥50 cm. Essa taxa de alarmes falsos inviabiliza declarar o classificador operacional.

## Limitações transversais

1. As datas e horários reais de disponibilidade dos dados ainda precisam ser auditados; previsões D+1 retrospectivas não comprovam antecedência útil de 24 horas.
2. Há lacunas críticas de chuva e nível em outubro de 2023; ausência de observação não é chuva zero.
3. As bases processadas foram incorporadas à branch de revisão, mas isso não comprova procedência integral, termos de redistribuição nem validação de metadados oficiais.
4. Não há teste independente documentado após a publicação no GitHub.
5. Falta publicar previsões individuais e alguns scripts históricos para permitir reprodução completa.

**Conclusão:** o projeto contém evidências de pesquisa exploratória, não validação de sistema de alerta de enchentes. Próximo passo técnico: auditar os dados por estação e evento, executar pipeline reproduzível e comparar falsos alarmes e antecedência com baselines.
