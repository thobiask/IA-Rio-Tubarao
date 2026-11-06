# Diagnóstico de execução independente — V69 a V73

Data da revisão: 2026-11-06. Escopo: inspeção estática dos scripts presentes em `revisao-inicial`. **Nenhum treinamento ou reexecução foi realizado nesta etapa.**

## Evidências no código publicado

| Versão | Script | Entrada/saída rígida identificada | Consequência |
|---|---|---|---|
| V69 | `experimentos/V69/reproduzir_v69.py` | `ROOT=Path('/mnt/data')`; entrada `base_ia_hidrologia_chuvas_3_estacoes.csv` | Não encontra a base em `dados/processados/` sem adaptação |
| V71 | `experimentos/V71/run_v71.py` | entrada `/mnt/data/base_tratada_ia_com_metadados.csv`; saída `/mnt/data/Rio_Tubarao_V71_selecao_estacoes` | Requer caminhos locais não versionados |
| V71 | `experimentos/V71/finalizar_v71.py` | `shutil.copy('/mnt/data/run_v71.py',...)` e `shutil.copy('/mnt/data/finalizar_v71.py',...)` | Pode falhar mesmo com saídas existentes; mistura finalização e empacotamento |
| V72 | `experimentos/V72/experimento_v72.py` | `SOURCE=Path('/mnt/data/base_tratada_ia_com_metadados.csv')`; saídas sob pasta do script | Entrada não corresponde ao caminho versionado |
| V73 | `experimentos/V73/experimento_v73.py` | `SOURCE=Path('/mnt/data/base_tratada_ia_com_metadados.csv')`; saídas sob pasta do script | Entrada não corresponde ao caminho versionado |

Entradas já publicadas:
- `dados/processados/base_ia_hidrologia_chuvas_3_estacoes.csv`
- `dados/processados/base_tratada_ia_com_metadados.csv`

## Política de preservação

1. Não editar os scripts históricos apenas para fazê-los rodar: manter versões originais para auditoria.
2. Criar wrappers/execução parametrizada em `scripts/reproducao/` ou versões explicitamente marcadas como adaptadas.
3. Registrar versões exatas de Python, pandas, NumPy, scikit-learn e bibliotecas auxiliares.
4. Reexecutar em diretório temporário, nunca sobrescrever resultados originais de `resultados/`.
5. Comparar arquivos por hash quando houver identidade byte a byte; para métricas numéricas, aplicar tolerância declarada e registrar divergências.
6. Verificar datas, fuso, disponibilidade temporal e possíveis vazamentos antes de atribuir validade operacional.

## Sequência proposta

- **Etapa 1:** verificação estrutural de todos os arquivos, cabeçalhos, datas, duplicidades e tamanhos.
- **Etapa 2:** inventário de dependências e execução adaptada da V69.
- **Etapa 3:** reprodução da V71, V72 e V73 em ambiente isolado.
- **Etapa 4:** comparação com saídas originais e relatório de divergências.
- **Etapa 5:** validação hidrológica dos eventos críticos, sem pressupor dados horários.

### Critério de conclusão

O experimento só será marcado **reproduzido** após execução efetiva, comparação registrada e aprovação dos critérios de consistência. Esta nota documenta apenas os obstáculos identificados por leitura do código.
