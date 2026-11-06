# Guia de navegação do repositório

O projeto reúne dados hidrológicos históricos, algoritmos de aprendizado de máquina, previsões retrospectivas e análises de desempenho para a bacia do Rio Tubarão.

## Por onde começar

O [README principal](../README.md) apresenta o problema investigado, as variáveis, os algoritmos, os resultados e as limitações.

Para aprofundar cada parte:

| Tema | Documento de referência |
|---|---|
| Visão geral e conclusões | [README](../README.md) |
| Estrutura dos dados e variáveis | [Dicionário de dados](DICIONARIO_DADOS.md) |
| Comparação de estações | [Relatório de seleção de estações](../resultados/V71/RELATORIO_V71.md) |
| Tratamento de ausências | [Relatório de dados incompletos](../resultados/V72/RELATORIO_V72.md) |
| Classificação de elevações | [Auditoria das previsões](AUDITORIA_PREVISOES_V73.md) |
| Cobertura de eventos críticos | [Relatório de cobertura](../resultados/V69/RELATORIO_V69.md) |
| Estado da reprodução | [Reprodutibilidade](REPRODUTIBILIDADE.md) |
| Inventário dos arquivos | [Bases publicadas](../inventario/BASES_HIDROLOGICAS_PENDENTES.md) |

## Estrutura

- [`dados/`](../dados/) contém os CSVs de chuva e bases hidrológicas processadas.
- [`experimentos/`](../experimentos/) contém os scripts históricos.
- [`resultados/`](../resultados/) reúne previsões, métricas e relatórios.
- [`scripts/`](../scripts/) contém rotinas auxiliares de auditoria.
- [`documentacao/`](./) registra decisões, limitações e verificações.
- [`inventario/`](../inventario/) registra arquivos e integridade.

A numeração das pastas identifica conjuntos históricos de experimentos. A apresentação científica é organizada pelos problemas investigados, não pela quantidade de versões.

## Situação dos materiais

Os arquivos principais foram publicados na branch de revisão. A presença dos CSVs e scripts está confirmada, mas a integridade byte a byte das bases remotas e a reprodução independente dos resultados ainda não foram certificadas. Os modelos não constituem sistema operacional de alerta.
