# Inteligência artificial aplicada ao monitoramento hidrológico do Rio Tubarão

## Apresentação

Este projeto investiga o uso de técnicas de aprendizado de máquina para analisar séries históricas de níveis fluviais na bacia do Rio Tubarão, em Santa Catarina. O objetivo é verificar se informações de diferentes estações hidrológicas permitem estimar o nível do rio no dia seguinte e reconhecer situações de elevação acentuada.

A motivação está na dificuldade de antecipar mudanças rápidas no comportamento dos rios, especialmente quando as medições disponíveis são incompletas. A pesquisa busca compreender tanto o potencial dos algoritmos quanto suas limitações diante das características dos dados hidrológicos.

Os experimentos são retrospectivos e utilizam dados diários. Portanto, os resultados não constituem um sistema de alerta de enchentes em tempo real.

## Objetivo e problema investigado

O problema central consiste em estimar a cota fluvial de um dia a partir das medições disponíveis até o dia anterior. Também é investigada a classificação de elevações diárias de pelo menos 50 ou 100 centímetros.

Duas perguntas orientam a análise. A primeira é se os modelos de aprendizado de máquina conseguem prever o nível com erros menores do que uma estimativa simples baseada no último valor observado. A segunda é se a utilização de medições de estações auxiliares melhora as previsões, inclusive quando parte dessas informações está ausente.

## Base de dados e área de estudo

A estação utilizada como referência principal é a de código **84580000**, identificada como Rio do Pouso, em Tubarão. Outras quatro estações são consideradas como fontes auxiliares:

| Código | Estação |
|---|---|
| 84580000 | Rio do Pouso, Tubarão |
| 84300000 | Pedras Grandes |
| 84560000 | São Ludgero |
| 84559800 | Braço do Norte |
| 84249998 | Orleans Montante |

As séries consolidadas estão disponíveis em [dados/processados](dados/processados/), enquanto os arquivos de precipitação estão organizados em [dados/chuva](dados/chuva/).

As medições passam por filtros de qualidade e consistência. Nos experimentos de previsão descritos aqui, foram considerados registros de nível classificados como de qualidade estrita, dentro da faixa de valores definida nos scripts, com exclusão de duplicidades conflitantes por data e estação. Os dados são organizados cronologicamente, preservando as lacunas existentes.

As bases incluem informações históricas de chuva, nível e vazão, mas os modelos de previsão apresentados nos resultados principais utilizam essencialmente **níveis fluviais e suas variações anteriores**. A presença de dados de chuva no repositório não significa que tenham sido utilizados como entrada em todos os modelos.

## Metodologia

### Preparação das variáveis

Para prever o nível do dia seguinte, os modelos recebem informações sobre o nível atual da estação principal, níveis observados nos dias anteriores e diferenças entre medições consecutivas. Quando disponíveis, também são considerados níveis atuais e anteriores das quatro estações auxiliares.

O valor a prever é o nível da estação principal no dia seguinte, expresso em centímetros. Nos experimentos de classificação, o objetivo passa a ser identificar se a diferença entre o nível do dia seguinte e o nível atual alcança um dos limites investigados.

A divisão dos dados é temporal: registros até 2015 são utilizados no treinamento; registros de 2016 a 2020 compõem a validação; e os dados elegíveis a partir de 2021 são reservados para teste. A quantidade efetiva de observações varia conforme a disponibilidade das variáveis exigidas por cada experimento.

### Algoritmos empregados

**Regressão Ridge.** Modelo de regressão linear com regularização, empregado para estimar a cota do dia seguinte. A regularização limita a influência excessiva dos coeficientes e oferece uma referência interpretável para comparar combinações de estações.

**HistGradientBoosting para regressão.** Algoritmo baseado na combinação sucessiva de árvores de decisão, utilizado para investigar relações não lineares entre as medições e o nível futuro.

**Regressão logística.** Modelo de classificação utilizado para estimar a probabilidade de uma elevação diária atingir os limites de 50 ou 100 centímetros.

**HistGradientBoosting para classificação.** Abordagem não linear empregada na mesma tarefa de classificação, permitindo comparar diferentes estratégias de identificação de elevações.

**Persistência.** Método de referência que assume que o nível do dia seguinte será igual ao nível atual. Embora não seja um algoritmo de aprendizado de máquina, sua comparação é indispensável para verificar se a maior complexidade dos modelos produz benefício real.

### Tratamento de medições ausentes

Uma dificuldade relevante é que as estações não apresentam registros completos nos mesmos dias. Inicialmente, foram comparados modelos em um conjunto de datas nas quais todas as entradas estavam disponíveis. Depois, foram avaliadas abordagens que permitem utilizar parte das estações auxiliares mesmo quando faltam medições.

Para o modelo Ridge multifonte, as ausências são tratadas por imputação pela mediana calculada no conjunto de treinamento, acompanhada de indicadores que informam quais variáveis estavam disponíveis. O HistGradientBoosting também foi avaliado com entradas ausentes.

Essa estratégia amplia a quantidade de dias que podem ser analisados, sem criar medições hidrológicas inexistentes.

## Resultados

### Contribuição das estações auxiliares

Em uma comparação realizada sobre **221 dias de teste comuns a todas as configurações**, o modelo Ridge com as estações auxiliares apresentou erro absoluto médio (MAE) de **21,075 cm**. O método de persistência apresentou **25,448 cm** na mesma amostra.

A retirada de Pedras Grandes ou São Ludgero aumentou o erro médio global nessa comparação. Isso indica que, no conjunto analisado, as estações contribuíram para a previsão. Entretanto, o resultado não significa que todas as estações sejam igualmente importantes em qualquer período.

Os detalhes estão no [relatório de seleção de estações](resultados/V71/RELATORIO_V71.md).

### Previsão com dados incompletos

Ao permitir medições auxiliares ausentes, foi possível avaliar **933 dias de teste** com histórico suficiente da estação principal, em vez de somente 221 dias com todas as estações disponíveis.

| Método | MAE (cm) | RMSE (cm) |
|---|---:|---:|
| Persistência | **22,147** | 50,550 |
| Ridge utilizando apenas a estação principal | 23,744 | 48,789 |
| Ridge multifonte com tratamento de ausências | 23,378 | **46,643** |
| HistGradientBoosting multifonte | 22,782 | 49,899 |

O **MAE** representa a média dos erros absolutos, enquanto o **RMSE** atribui maior peso aos erros de grande magnitude. O Ridge multifonte obteve o menor RMSE, mas a persistência apresentou o menor MAE. Portanto, os resultados não demonstram superioridade geral de um único modelo.

O [relatório de tratamento de dados ausentes](resultados/V72/RELATORIO_V72.md) apresenta os recortes e as comparações.

### Identificação de elevações acentuadas

A classificação de subidas diárias foi investigada com limites de 50 e 100 centímetros. No conjunto de teste de **933 dias**, ocorreram **55 subidas observadas de pelo menos 50 cm**.

Uma configuração de regressão logística, com limiar de decisão selecionado na validação, identificou **35 dessas subidas**, mas também gerou **451 classificações positivas incorretas**. Sua precisão foi de aproximadamente **7,2%**, com recall de **63,6%**.

Isso evidencia uma dificuldade central da classificação de eventos relativamente raros: aumentar a quantidade de eventos identificados pode produzir um número elevado de falsos alarmes. Uma elevação de 50 cm, por si só, também não demonstra ocorrência de inundação.

A [auditoria das previsões de classificação](documentacao/AUDITORIA_PREVISOES_V73.md) documenta essa avaliação.

## Limitações

As séries utilizadas nos experimentos principais possuem resolução diária. Não é possível determinar, apenas com essas observações, a hora exata de uma subida ou a antecedência que um eventual alerta poderia oferecer.

Existem lacunas relevantes em períodos de interesse, incluindo outubro de 2023. A disponibilidade das medições no momento em que uma previsão teria sido emitida ainda exige conferência. Também é necessário validar integralmente os metadados oficiais das estações e a origem dos arquivos.

Os códigos históricos foram preservados, mas alguns utilizam caminhos locais absolutos, como `/mnt/data/`. A execução independente em outro ambiente ainda não foi validada. O [diagnóstico de reprodutibilidade](documentacao/DIAGNOSTICO_EXECUCAO_INDEPENDENTE.md) descreve os ajustes e verificações necessários.

## Conclusão

Os experimentos mostram que informações de diferentes estações podem contribuir para a previsão de níveis fluviais em determinadas condições. Também demonstram que o tratamento de medições ausentes permite aproveitar um número maior de observações históricas.

Entretanto, a comparação com a persistência revela que modelos mais complexos não apresentam necessariamente menores erros médios. Na classificação de elevações, a elevada quantidade de falsos positivos indica a necessidade de aperfeiçoar a metodologia e ampliar a validação antes de qualquer aplicação prática.

O desenvolvimento futuro depende principalmente de séries com melhor cobertura temporal, verificação dos horários reais das medições, reprodução independente dos resultados e avaliação específica de eventos hidrológicos críticos.

## Organização dos arquivos

| Diretório | Conteúdo |
|---|---|
| [dados](dados/) | Séries hidrológicas e precipitação |
| [experimentos](experimentos/) | Implementações dos algoritmos e testes históricos |
| [resultados](resultados/) | Previsões, métricas e relatórios técnicos |
| [scripts](scripts/) | Rotinas auxiliares de processamento e auditoria |
| [documentacao](documentacao/) | Metodologia, verificações e limitações |
| [inventario](inventario/) | Controle dos arquivos e pendências documentais |

Os nomes numéricos de algumas pastas são identificadores internos dos experimentos e foram mantidos para preservar a correspondência entre códigos, resultados e relatórios.
