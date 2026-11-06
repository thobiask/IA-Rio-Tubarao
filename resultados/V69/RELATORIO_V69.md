# V69 — Diagnóstico de prontidão para séries subdiárias

**Data:** 30/10/2026. **Escopo:** auditoria local e plano de aquisição; **não** foram obtidos dados horários novos, nem treinados novos modelos.

## 1. Evidências disponíveis

- Base consolidada: `base_ia_hidrologia_chuvas_3_estacoes.csv`; 140,103 registros; 10 códigos de estação.
- A coluna `data` é diária no conjunto consolidado; timestamps à meia-noite não demonstram observação à meia-noite.
- Foram inspecionados 4 arquivos internos de 4 ZIPs de chuva. A presença de CSV de chuva **não** comprova resolução horária.
- A V68 já documentou ausências críticas de chuva em outubro/2023 e falhas em elevações de maio/2022.

## 2. Cobertura de nível nos episódios (base local)

| episodio     |   codigo |   dias_janela |   dias_com_nivel |   dias_nivel_estrito |   dias_sem_nivel |
|:-------------|---------:|--------------:|-----------------:|---------------------:|-----------------:|
| maio_2022    | 84249998 |            16 |               16 |                   16 |                0 |
| maio_2022    | 84300000 |            16 |               16 |                    9 |                0 |
| maio_2022    | 84559800 |            16 |               16 |                   16 |                0 |
| maio_2022    | 84560000 |            16 |               16 |                   10 |                0 |
| maio_2022    | 84580000 |            16 |               16 |                   11 |                0 |
| outubro_2023 | 84249998 |            25 |                0 |                    0 |               25 |
| outubro_2023 | 84300000 |            25 |               12 |                    0 |               13 |
| outubro_2023 | 84559800 |            25 |               25 |                   25 |                0 |
| outubro_2023 | 84560000 |            25 |                0 |                    0 |               25 |
| outubro_2023 | 84580000 |            25 |                7 |                    7 |               18 |

**Nota:** o filtro estrito foi inferido da coluna `nivel_cm_qualidade_estrita`; a V68 é a referência para pares de previsão elegíveis. Contagem de dias não equivale a avaliação de acertos de alerta.

## 3. Cobertura de chuva diária

| episodio     | variavel                    |   dias_janela |   dias_com_valor |   dias_sem_valor |
|:-------------|:----------------------------|--------------:|-----------------:|-----------------:|
| maio_2022    | chuva_orleans_mm_dia        |            16 |               16 |                0 |
| maio_2022    | chuva_braco_do_norte_mm_dia |            16 |               16 |                0 |
| maio_2022    | chuva_tubarao_mm_dia        |            16 |               16 |                0 |
| outubro_2023 | chuva_orleans_mm_dia        |            25 |                0 |               25 |
| outubro_2023 | chuva_braco_do_norte_mm_dia |            25 |                0 |               25 |
| outubro_2023 | chuva_tubarao_mm_dia        |            25 |                0 |               25 |

A ausência de valor é lacuna de observação, não chuva zero. Mesmo chuva diária presente pode não estar disponível no instante de emissão da previsão.

## 4. Resultados da auditoria V68 a preservar

- Maio/2022: 61 pares elegíveis para subida ≥50 cm, 12 subidas reais elegíveis, 6 detectadas e 13 falsos positivos.
- Outubro/2023: Braço do Norte, 25 pares elegíveis, 4 subidas, 2 detectadas e 12 falsos positivos; Rio do Pouso, 7 pares elegíveis, 2 subidas, 0 detectadas.
- Elevações de um dia para outro **não** informam a hora da subida, tempo de propagação ou antecedência de alerta.

## 5. O que precisa ser obtido antes do próximo treinamento

1. **Inventário oficial ANA:** confirmar código, nome, localização, datum, tipo de medição e operação das cinco estações.
2. **Séries subdiárias:** consultar ANA HidroWebService (telemetria adotada/detalhada), SGB e fontes locais, sem presumir disponibilidade.
3. **Chuva:** verificar CEMADEN, Defesa Civil e telemetria ANA, documentando cobertura e latência.
4. **Metadados obrigatórios:** `estacao_codigo`, `timestamp_original`, `fuso`, `timestamp_utc`, `variavel`, `valor`, `unidade`, `status_qualidade`, `fonte`, `data_extracao`, `tipo_tempo` (observação/transmissão).
5. **Critérios de aceite:** cobertura em maio/2022 e outubro/2023; ausência de duplicidades conflitantes; intervalos efetivos medidos; fuso validado; não interpolar lacunas críticas; comparações de nível apenas com referência local de régua.

**Fontes técnicas já identificadas na V63:** https://www.ana.gov.br/hidrowebservice/swagger-ui/index.html e manual em https://www.gov.br/ana/pt-br/assuntos/monitoramento-e-eventos-criticos/monitoramento-hidrologico/orientacoes-manuais/manuais/manual-hidrowebservice_publica.pdf . A API pode requerer cadastro e credenciais.

## 6. Plano experimental após aquisição

- Comparar horizontes de **3, 6, 12 e 24 horas**, apenas nas estações com séries realmente adequadas.
- Baselines: persistência, Ridge, Random Forest, Gradient Boosting; MLP como hipótese adicional.
- Divisão temporal sem vazamento; validação por eventos independentes; registrar MAE/RMSE, recall, precisão, falsos alarmes e antecedência.
- Não chamar subida de ≥50 cm de enchente sem rótulos de impactos ou limiares oficiais validados.

## 7. Próxima ação operacional

Preencher `plano_aquisicao_subdiaria.csv` com consulta oficial por código e janela; salvar arquivos brutos imutáveis, metadados e comprovantes de origem. Somente então iniciar V70 (comparação com dados subdiários).

## 8. Arquivos gerados

- `diagnostico_cobertura_eventos.csv` — nível por estação e janela.
- `cobertura_chuva_eventos.csv` — cobertura diária por variável.
- `inventario_arquivos_chuva.csv` — arquivos locais de chuva.
- `plano_aquisicao_subdiaria.csv` — checklist operacional.
- `MANIFESTO.json` — integridade da base consolidada.
