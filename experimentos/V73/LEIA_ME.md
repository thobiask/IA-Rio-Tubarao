# Classificação de elevações diárias

Este experimento investiga a classificação de elevações do nível fluvial de **50 cm** e **100 cm** entre dias consecutivos na estação Rio do Pouso, em Tubarão.

O script histórico [`experimento_v73.py`](experimento_v73.py) compara regressão logística e HistGradientBoostingClassifier. As entradas incluem níveis recentes da estação principal, diferenças entre medições e dados auxiliares disponíveis. O limiar de classificação é selecionado no conjunto de validação.

As saídas estão em [`resultados/V73/`](../../resultados/V73/). A [auditoria das previsões](../../documentacao/AUDITORIA_PREVISOES_V73.md) examina as classificações e os falsos positivos.

No teste retrospectivo de 933 dias, a configuração de regressão logística analisada na auditoria identificou 35 das 55 subidas de pelo menos 50 cm, mas produziu 451 falsos positivos. A precisão de aproximadamente 7,2% não sustenta aplicação operacional.

O script original utiliza o caminho `/mnt/data/base_tratada_ia_com_metadados.csv` e depende principalmente de `numpy`, `pandas` e `scikit-learn`. A versão exata do ambiente e a reexecução independente ainda não foram verificadas.

Subidas diárias de nível não são sinônimo de inundação ou de alerta oficial.
