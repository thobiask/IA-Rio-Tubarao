# IA Rio Tubarão — pesquisa hidrológica

Repositório privado de revisão da pesquisa exploratória de previsão de níveis e detecção de elevações na bacia do Rio Tubarão (SC).

> **Pesquisa retrospectiva. Não é um sistema operacional de alerta de enchentes.**

## Organização prevista
- `dados/`: séries hidrológicas e precipitação, após auditoria.
- `scripts/`: rotinas de tratamento, modelagem e validação.
- `experimentos/`: implementações por versão.
- `resultados/`: relatórios, métricas e previsões.
- `documentacao/`: metodologia, decisões e limitações.
- `inventario/`: manifesto de arquivos e hashes SHA-256.

## Estado
A estrutura inicial foi criada. As bases ainda **não foram publicadas** e serão revisadas antes do envio. V60–V73 são experimentos retrospectivos, não evidência de confiabilidade operacional. O teste MLP foi exploratório.

## Controles antes de publicar dados
1. Conferir licenças e proveniência (ANA e demais fontes).
2. Verificar informações pessoais, segredos e metadados.
3. Validar integridade e correspondência com manifesto.
4. Testar scripts em ambiente limpo.
5. Revisar os resultados científicos antes de tornar o repositório público.
