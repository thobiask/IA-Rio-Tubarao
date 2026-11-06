# IA Rio Tubarão — previsão exploratória de níveis fluviais com inteligência artificial

**Projeto acadêmico de pesquisa aplicada à bacia do Rio Tubarão (Santa Catarina, Brasil).**

> **Aviso:** os resultados são retrospectivos e exploratórios. Este repositório **não é um sistema operacional de previsão ou alerta de enchentes**. Não utilizar os modelos para decisões de segurança pública.

## 1. Qual é o problema?

O nível de um rio depende de chuvas, condições hidrológicas anteriores e comportamento da bacia. O projeto investiga se dados históricos de nível e de estações próximas podem ajudar algoritmos de aprendizado de máquina a estimar **o nível do dia seguinte** e a identificar **elevações diárias acentuadas**. A pergunta central é se esses algoritmos oferecem vantagens mensuráveis sobre uma regra simples: assumir que o nível de amanhã será igual ao de hoje (**persistência**).

A pesquisa também avalia problemas práticos: lacunas de medição, estações com cobertura desigual e desempenho durante subidas rápidas. Não há comprovação de disponibilidade horária em tempo real.

## 2. Dados e estação-alvo

A principal estação-alvo dos experimentos V71–V73 é **84580000 — Rio do Pouso, Tubarão**. As quatro estações auxiliares analisadas são **84300000 (Pedras Grandes), 84560000 (São Ludgero), 84559800 (Braço do Norte) e 84249998 (Orleans-Montante)**.

As bases locais publicadas estão em:
- [`dados/processados/`](dados/processados/) — séries consolidadas de nível, vazão e chuva e metadados de tratamento.
- [`dados/chuva/`](dados/chuva/) — séries e acumulados de precipitação.

**Atenção:** a procedência, os metadados oficiais, as licenças de redistribuição e a disponibilidade temporal das observações ainda precisam de auditoria integral. Um valor diário com data não comprova que estivesse disponível no instante de emissão da previsão. A identificação da estação 84580000 foi corrigida documentalmente em relação a um rótulo equivocado na base histórica.

## 3. Onde está a inteligência artificial?

| Abordagem | Uso no projeto |
|---|---|
| **Ridge Regression** | Prever o nível fluvial em D+1 a partir de níveis e variações recentes |
| **HistGradientBoosting (regressão)** | Modelar relações não lineares para previsão de nível |
| **Regressão logística** | Classificar subidas diárias de pelo menos 50 ou 100 cm |
| **HistGradientBoosting (classificação)** | Comparar classificação não linear de subidas |
| **Persistência** | Baseline sem aprendizado de máquina, usado para testar se a IA realmente agrega valor |

Os modelos usam séries temporais históricas. Nos experimentos de previsão e classificação, o recorte declarado é **treino até 2015, validação entre 2016 e 2020 e teste a partir de 2021**, limitado às datas elegíveis disponíveis. Essa separação temporal reduz comparações indevidas, mas não substitui a auditoria de disponibilidade real de cada dado.

## 4. Etapas da pesquisa

A pesquisa foi organizada por **problemas investigados**, e não pela numeração dos testes. O leitor pode consultar diretamente os materiais correspondentes:

| Etapa | Pergunta investigada | Materiais |
|---|---|---|
| Diagnóstico das séries | Quais dados faltam nos episódios críticos? | [Relatório de cobertura](resultados/V69/RELATORIO_V69.md) · [Código](experimentos/V69/reproduzir_v69.py) |
| Qualidade e aquisição | Como auditar dados e avaliar a necessidade de séries subdiárias? | [Rotinas de auditoria](scripts/V70/) |
| Seleção de estações | Excluir estações melhora a previsão? | [Resultados](resultados/V71/RELATORIO_V71.md) · [Código](experimentos/V71/) |
| Tratamento de dados ausentes | Como prever com medições auxiliares incompletas? | [Resultados](resultados/V72/RELATORIO_V72.md) · [Código](experimentos/V72/) |
| Classificação de elevações | É possível identificar subidas diárias relevantes? | [Método](experimentos/V73/LEIA_ME.md) · [Código](experimentos/V73/) · [Auditoria](documentacao/AUDITORIA_PREVISOES_V73.md) |

A numeração interna das pastas é mantida apenas para **rastreabilidade dos arquivos e experimentos**, não como elemento central da apresentação acadêmica.

## 5. Resultados principais

### Previsão de nível com múltiplas estações

Em **221 dias de teste com todas as estações disponíveis**, o Ridge multifonte apresentou **MAE de 21,075 cm**, frente a **25,448 cm** da persistência. Excluir Pedras Grandes ou São Ludgero piorou o MAE global nessa mesma coorte. **Não comparar diretamente MAEs de coortes com datas diferentes.** [Detalhes](resultados/V71/RELATORIO_V71.md).

### Tratamento de medições ausentes

A avaliação retrospectiva com histórico suficiente da estação-alvo passou de **221 para 933 dias**, ao permitir ausência das auxiliares. Nas **933 datas comuns**:

| Modelo | MAE (cm) | RMSE (cm) |
|---|---:|---:|
| Persistência | **22,147** | 50,550 |
| Ridge só alvo | 23,744 | 48,789 |
| Ridge multifonte com faltantes | 23,378 | **46,643** |
| HistGradientBoosting multifonte | 22,782 | 49,899 |

O Ridge multifonte teve o menor RMSE, mas **não superou a persistência em MAE**. [Detalhes](resultados/V72/RELATORIO_V72.md).

### Classificação de elevações diárias

No teste com **933 dias**, ocorreram **55 subidas observadas de pelo menos 50 cm**. A regressão logística com limiar ajustado na validação identificou **35**, mas produziu **451 falsos positivos** (precisão de aproximadamente **7,2%**). Esse resultado é inadequado para declarar capacidade de alerta operacional. Uma subida de 50 cm **não equivale automaticamente a inundação**. [Auditoria](documentacao/AUDITORIA_PREVISOES_V73.md).

## 6. Como o professor pode examinar o trabalho?

1. Ler este README para conhecer a pergunta, os algoritmos e as conclusões.
2. Consultar os relatórios de previsão, tratamento de dados ausentes e classificação, com métricas e limitações.
3. Examinar os scripts históricos em [`experimentos/`](experimentos/) e as saídas em [`resultados/`](resultados/).
4. Consultar a [auditoria de execução independente](documentacao/DIAGNOSTICO_EXECUCAO_INDEPENDENTE.md) antes de tentar reproduzir os modelos.

**Estado de reprodução:** os scripts originais foram preservados e ainda contêm caminhos absolutos como `/mnt/data/`. Portanto, **não há execução independente validada em ambiente limpo**; é necessário ajustar caminhos em uma cópia ou wrapper, registrar versões das bibliotecas e comparar os resultados obtidos com os arquivos originais. Não executar diretamente esperando que funcionem sem adaptação.

## 7. Organização do repositório

```text
dados/          Bases hidrológicas e precipitação
experimentos/   Scripts históricos separados por versão
resultados/     Métricas, previsões e relatórios originais
scripts/        Ferramentas de auditoria e processamento
documentacao/   Método, histórico, auditorias e limitações
inventario/     Inventário de arquivos, integridade e pendências
```

## 8. Limitações e próximos passos

- Confirmar os metadados oficiais e os direitos de redistribuição das séries.
- Auditar os horários reais de observação/transmissão e as lacunas, especialmente em **outubro de 2023**.
- Executar os scripts em ambiente isolado, com dependências e entradas registradas.
- Validar desempenho por eventos independentes e por estação, incluindo falsos alarmes.
- Só investigar previsão subdiária (3, 6, 12 ou 24 horas) após obter séries efetivamente compatíveis com esses horizontes.

**Leitura complementar:** [reprodutibilidade](documentacao/REPRODUTIBILIDADE.md) · [auditoria comparativa](documentacao/AUDITORIA_COMPARATIVA_V71_V73.md) · [diagnóstico V69](resultados/V69/RELATORIO_V69.md).

---

**Situação do projeto:** documentação acadêmica em revisão na branch `revisao-inicial`. Os dados e resultados publicados são históricos; a pesquisa não fornece alertas oficiais nem previsões operacionais.
