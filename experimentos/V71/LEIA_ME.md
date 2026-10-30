# V71 — seleção de estações (registro de reprodução)

## Arquivos originais
- `run_v71.py`: implementação histórica de regressão Ridge e persistência, com cenários A (todas), B (sem Pedras Grandes), C (sem São Ludgero), D (só alvo).
- `../../resultados/V71/metricas_v71.csv`: resultados históricos por protocolo, cenário e recorte.
- `../../resultados/V71/cobertura_v71.csv`: contagem de dias elegíveis por cenário.
- `../../resultados/V71/diferencas_bootstrap_v71.csv`: diferenças e intervalos bootstrap.

## Como reproduzir
O script histórico depende de `pandas`, `numpy` e `scikit-learn` e procura a base em `/mnt/data/base_tratada_ia_com_metadados.csv`. Também escreve em `/mnt/data/Rio_Tubarao_V71_selecao_estacoes`. Esses caminhos são parte do código original; ainda não foram parametrizados.

**Não execute diretamente sem conferir a procedência da base e a versão das bibliotecas.**

## Interpretação importante
O protocolo `fixo` usa 221 dias comuns de teste e permite comparar os cenários de forma pareada. O protocolo `disponibilidade` muda o conjunto de dias elegíveis (221, 311, 223 ou 933 dias), portanto seus MAEs não devem ser comparados como se fossem observações idênticas.

Os recortes `subidas_50cm` e `subidas_100cm` são definidos a posteriori, a partir do nível observado no dia seguinte. Isso não equivale a uma classificação antecipada de enchentes.

## Estado
- [x] Código original `run_v71.py` publicado e hash Git conferido.
- [x] Métricas e cobertura publicadas.
- [ ] `finalizar_v71.py` e relatório integral.
- [ ] Reexecução independente.
- [ ] Bases de entrada auditadas.
