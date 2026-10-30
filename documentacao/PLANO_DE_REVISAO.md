# Plano de revisão do projeto IA Rio Tubarão

## Etapa 1 — organização e proveniência
- [ ] Conferir inventário, origem, hashes SHA-256 e duplicidades.
- [ ] Identificar licenças e atribuições exigidas para redistribuir cada base.
- [ ] Conferir códigos e localização de estações hidrométricas.
- [ ] Verificar dados pessoais e credenciais.

## Etapa 2 — metodologia
- [ ] Documentar partição temporal: treinamento até 2015; validação 2016–2020; teste 2021–2025, conforme cada experimento.
- [ ] Distinguir regressão de nível, classificação de elevação e alerta de enchente.
- [ ] Comparar persistência, Ridge, Random Forest e Gradient Boosting.
- [ ] Tratar o MLP como estudo exploratório separado.
- [ ] Auditar disponibilidade e lacunas nos eventos de 2022 e 2023.

## Etapa 3 — V69–V73
- [ ] Conferir scripts, dependências e resultados em ambiente limpo.
- [ ] Validar comparações pareadas, evitar vazamento temporal e documentar tratamento de dados faltantes.
- [ ] Avaliar recall, precisão, falsos positivos e antecedência por evento.
- [ ] Registrar limitações: não há sistema operacional de alerta validado.

## Etapa 4 — revisão antes da publicação pública
- [ ] Revisão científica, de licenças e de segurança.
- [ ] Publicar apenas dados e resultados cuja origem e integridade foram verificadas.
