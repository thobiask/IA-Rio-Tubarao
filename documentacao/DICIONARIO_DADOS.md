# Dicionário de dados

Este documento explica as variáveis mais relevantes identificadas nos scripts de modelagem e nos relatórios. **Não é um inventário exaustivo de todas as colunas de todos os CSVs.** A estrutura completa de cada arquivo deve ser conferida diretamente em seu cabeçalho.

## Variáveis hidrológicas

| Campo | Significado | Unidade ou formato |
|---|---|---|
| `data` | Data associada ao registro histórico | Data; horário efetivo não necessariamente conhecido |
| `estacao_codigo` | Identificador da estação hidrológica | Código |
| `nivel_cm` | Nível observado da estação | Centímetros |
| `nivel_m` | Nível expresso em metros, quando presente | Metros |
| `vazao_m3_s` | Vazão fluvial, quando presente | Metros cúbicos por segundo |
| `nivel_cm_qualidade_estrita` | Indicador de elegibilidade segundo o tratamento histórico | Valor lógico ou representação equivalente |
| `chuva_orleans_mm_dia` | Precipitação diária associada a Orleans | Milímetros por dia |
| `chuva_braco_do_norte_mm_dia` | Precipitação diária associada a Braço do Norte | Milímetros por dia |
| `chuva_tubarao_mm_dia` | Precipitação diária associada a Tubarão | Milímetros por dia |

As variáveis de chuva foram identificadas na base consolidada e no diagnóstico de cobertura. Outros acumulados de 24, 48 e 72 horas podem estar presentes nos arquivos de precipitação. Sua definição exata e a convenção de fechamento de cada janela precisam ser conferidas na origem.

## Variáveis derivadas dos experimentos

| Campo ou conceito | Interpretação |
|---|---|
| `alvo_lag0` | Nível atual da estação-alvo |
| `alvo_lag1`, `alvo_lag2`, `alvo_lag3` | Níveis observados em dias anteriores |
| `alvo_delta1`, `alvo_delta2` | Diferenças entre níveis consecutivos |
| `y` ou `y_prox` | Nível observado no dia seguinte, usado como alvo |
| `nivel_atual` | Nível disponível no dia de emissão |
| `subida_cm` | Diferença entre o nível do dia seguinte e o nível atual |
| `data_emissao` | Data de referência da previsão retrospectiva |
| `data_alvo` | Dia a que a previsão se refere |
| `observado_cm` | Nível observado na data-alvo |
| `previsto_cm` | Nível estimado pelo modelo |
| `persistencia_cm` | Estimativa baseada na manutenção do nível atual |
| `n_aux_disponiveis` | Quantidade de entradas auxiliares presentes na linha do experimento |
| `*_presente` | Indicador de disponibilidade de uma variável auxiliar |

## Métricas

**MAE** é a média dos erros absolutos entre valores observados e previstos. **RMSE** é a raiz do erro quadrático médio e atribui maior peso a erros grandes. **Precisão** é a proporção de classificações positivas que correspondem a eventos reais. **Recall** é a proporção de eventos reais identificados. **Falsos positivos** são alertas de elevação sem ocorrência da subida definida no experimento.

## Cuidados de interpretação

A cota medida em uma estação depende de sua referência local e não deve ser comparada diretamente com a de outra estação sem validação do datum. Uma data diária não comprova a hora de medição ou transmissão. Valores ausentes não equivalem a zero. O limiar de elevação de 50 ou 100 cm é uma definição experimental e não um limiar oficial de inundação.
