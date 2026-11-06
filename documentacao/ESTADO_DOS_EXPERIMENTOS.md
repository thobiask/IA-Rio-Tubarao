# Estado dos experimentos

O desenvolvimento está organizado por objetivos científicos. Os códigos numéricos das pastas identificam execuções históricas e não representam níveis de maturidade operacional.

| Investigação | Arquivos disponíveis | Estado de validação |
|---|---|---|
| Modelagem inicial e inclusão de chuva | Histórico resumido em [MAPA_VERSOES.md](MAPA_VERSOES.md) | Documentação e reprodução completas ainda não verificadas |
| Cobertura dos episódios críticos | [Relatório de cobertura](../resultados/V69/RELATORIO_V69.md) e [script](../experimentos/V69/reproduzir_v69.py) | Resultados históricos publicados; reexecução pendente |
| Auditoria de dados subdiários | [Documentação](../resultados/V70/LEIA_ME_V70.md) e [rotinas](../scripts/V70/) | Não comprova aquisição de dados horários |
| Seleção de estações | [Relatório](../resultados/V71/RELATORIO_V71.md), [scripts](../experimentos/V71/) e [previsões](../resultados/V71/previsoes_pareadas_v71.csv) | Comparações históricas disponíveis; reprodução independente pendente |
| Tratamento de dados ausentes | [Relatório](../resultados/V72/RELATORIO_V72.md), [script](../experimentos/V72/experimento_v72.py) e [previsões](../resultados/V72/previsoes_v72.csv) | Comparação histórica de 933 dias; reprodução independente pendente |
| Classificação de elevações | [Auditoria](AUDITORIA_PREVISOES_V73.md), [script](../experimentos/V73/experimento_v73.py) e [previsões](../resultados/V73/previsoes_v73.csv) | Falsos positivos elevados; reprodução independente pendente |

Os dados de entrada principais já estão presentes em [`dados/processados/`](../dados/processados/). Publicação de arquivo não significa integridade verificada nem resultado reproduzido.

Para uma explicação didática do estudo, consultar o [README principal](../README.md).
