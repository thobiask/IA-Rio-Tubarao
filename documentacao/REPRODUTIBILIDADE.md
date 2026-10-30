# Reprodutibilidade e limites de uso

Este repositório está em **revisão privada**. A publicação é incremental e **não certifica que os resultados foram reproduzidos em ambiente independente**.

## Convenções
- Nomes Vxx indicam versões experimentais, não versões operacionais.
- `dados/` guarda bases somente após conferência de origem, licença e integridade.
- `scripts/` contém implementações; caminhos absolutos locais existentes em versões históricas precisam ser parametrizados e testados antes de execução independente.
- `resultados/` contém métricas e saídas de testes retrospectivos.
- `inventario/` documenta origem e SHA-256 dos arquivos.
- Dados faltantes não devem ser tratados como zero, e não se devem inventar timestamps.
- A separação temporal treino/validação/teste e a disponibilidade real dos dados na data da previsão devem ser auditadas.
- Detecção de elevação de nível não equivale a detecção de enchente nem a alerta oficial.

## Status
A publicação das bases grandes e dos scripts completos depende de auditoria. Os arquivos publicados inicialmente são amostras **reais do pacote local**, não dados sintéticos, exceto testes explicitamente identificados como sintéticos.
