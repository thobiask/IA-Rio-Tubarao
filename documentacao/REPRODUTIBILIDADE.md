# Reprodutibilidade e limites de uso

O repositório reúne bases hidrológicas, scripts históricos, métricas e previsões retrospectivas. A publicação desses materiais **não comprova reprodução independente**.

## Dados de entrada

Os arquivos utilizados nos experimentos estão em [`dados/processados/`](../dados/processados/) e [`dados/chuva/`](../dados/chuva/). O inventário com hashes locais informados está em [`inventario/BASES_HIDROLOGICAS_PENDENTES.md`](../inventario/BASES_HIDROLOGICAS_PENDENTES.md). Ainda é necessário verificar os hashes dos arquivos remotos, a origem e as condições de redistribuição.

## Códigos e saídas

Os scripts originais estão em [`experimentos/`](../experimentos/) e os resultados em [`resultados/`](../resultados/). Alguns scripts usam caminhos absolutos `/mnt/data/`, que não correspondem aos caminhos internos do repositório. O [diagnóstico de execução independente](DIAGNOSTICO_EXECUCAO_INDEPENDENTE.md) registra esses impedimentos.

Para reproduzir corretamente, deve-se registrar o ambiente e as versões das bibliotecas, adaptar caminhos sem modificar silenciosamente os scripts históricos, executar em pasta isolada e comparar métricas e previsões com os arquivos publicados.

## Cuidados metodológicos

Os modelos usam separação cronológica entre treinamento, validação e teste. A disponibilidade efetiva das medições no instante da previsão ainda precisa de auditoria. Valores ausentes não devem ser confundidos com zero. Não se deve atribuir horários de observação a registros diários sem confirmação.

Uma elevação diária de 50 ou 100 cm não equivale automaticamente a enchente. Os resultados publicados não habilitam alertas operacionais.

## Estado

**Arquivos publicados:** confirmado. **Reexecução independente:** pendente. **Auditoria integral de integridade, proveniência e disponibilidade temporal:** pendente.
