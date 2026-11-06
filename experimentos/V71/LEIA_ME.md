# Seleção de estações auxiliares

Este experimento avalia a contribuição de quatro estações hidrológicas na previsão diária do nível da estação Rio do Pouso, em Tubarão.

O script [`run_v71.py`](run_v71.py) compara regressão Ridge e persistência em cenários com todas as estações, sem Pedras Grandes, sem São Ludgero e somente com a estação principal. O script [`finalizar_v71.py`](finalizar_v71.py) consolida análises complementares.

As métricas estão em [`resultados/V71/`](../../resultados/V71/), incluindo [relatório](../../resultados/V71/RELATORIO_V71.md), cobertura, diferenças bootstrap e previsões pareadas.

A comparação principal usa **221 dias comuns de teste**. As avaliações por disponibilidade usam conjuntos de dias diferentes (221, 311, 223 e 933), portanto não devem ser interpretadas como comparações pareadas.

Os scripts históricos dependem de `pandas`, `numpy` e `scikit-learn` e usam caminhos absolutos `/mnt/data/`. A reexecução independente ainda não foi validada.

Os recortes de subidas de 50 e 100 cm são definidos com base nas observações posteriores e não demonstram capacidade operacional de alerta.
