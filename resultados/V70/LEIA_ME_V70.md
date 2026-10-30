# V70 — Preparação para aquisição de séries subdiárias do Rio Tubarão

**Data:** 30/10/2026  
**Estado:** protocolo de consulta e ferramenta de auditoria preparados; **nenhuma série horária nova foi obtida neste pacote**.

## O que foi confirmado nas fontes oficiais
- A ANA disponibiliza `HidroinfoanaSerieTelemetricaDetalhada/v1` (dados adotados e brutos) e `HidroinfoanaSerieTelemetricaAdotada/v1` (dados adotados). Consulta por estação e período limitado a 30 dias.
- O manual oficial de 20/02/2026 informa autenticação com credenciais fornecidas mediante solicitação para `hidro@ana.gov.br`.
- O endpoint de consulta detalhada pede **Código da Estação**, **Tipo Filtro Data = DATA_LEITURA**, **Data de Busca** e **Range Intervalo de busca** (ex.: `DIAS_30`, `DIAS_21` ou `HORA_24`).
- A documentação distingue `Data_Hora_Medicao` de `Data_Atualizacao`; a primeira é a hora da observação, a segunda é atualização no banco.
- No exemplo da ANA, `Cota_Adotada` é expressa em cm, `Chuva_Adotada` em mm e `Vazao_Adotada` em m³/s; **confirmar metadados e significado de chuva para cada estação antes de acumular**.
- O manual lista qualidade `0=ok`, `1=suspeito`, `2=ruim` no exemplo. Não inferir qualidade quando campo ausente.
- A fonte oficial de inventário `HidroInventarioEstacoes/v1` é necessária para confirmar código, nome, coordenadas e operação; código de estação convencional **não garante** correspondência a código de estação telemétrica.

## Execução manual inicial (uma estação antes das demais)
1. Solicitar acesso à ANA, sem inserir credenciais em arquivos compartilhados.
2. Abrir https://www.ana.gov.br/hidrowebservice/swagger-ui/index.html
3. Autenticar seguindo o manual da ANA.
4. Consultar `HidroInventarioEstacoes/v1` por código. Registrar o resultado bruto e verificar se o código tem telemetria no período.
5. Consultar `HidroinfoanaSerieTelemetricaDetalhada/v1`, inicialmente um dia conhecido, com `DATA_LEITURA` e intervalo adequado. Confirmar a semântica do filtro antes de buscar janelas maiores.
6. Consultar os períodos `2022-04-27` a `2022-05-12` e `2023-10-01` a `2023-10-25`, em chamadas que não ultrapassem 30 dias; se a API usar data de referência e intervalo retrospectivo, ajustar conforme o resultado observado e documentar.
7. Salvar o JSON **original** em `brutos/` com nome `CODIGO_EVENTO.json`. Não sobrescrever.
8. Processar com `python auditar_json_ana.py brutos --saida saidas`. O script não cria timestamps artificiais nem converte fuso desconhecido.
9. Preencher `consultas_ana_v70.csv` com status e justificativa (inclusive indisponibilidade e respostas vazias).

## Aceite para modelagem
- Estação oficialmente identificada e com dados realmente subdiários em 2022/2023.
- Data/hora de medição presente; fuso horário explicitamente documentado antes de converter para UTC.
- Qualidade dos valores e lacunas examinadas; sem transformar `null` em zero.
- Nenhuma interpolação automática nos eventos críticos.
- Disponibilidade temporal das variáveis (chuva e nível) demonstrada antes de prever horizontes 3, 6, 12 e 24 horas.

## Comandos
```
python auditar_json_ana.py brutos --saida saidas
python testar_auditoria.py
```

**Atenção:** este é um protocolo de aquisição e auditoria, não uma demonstração de disponibilidade de telemetria nas cinco estações. Nenhum modelo foi treinado nesta versão.

Fontes:
- Manual ANA: https://www.gov.br/ana/pt-br/assuntos/monitoramento-e-eventos-criticos/monitoramento-hidrologico/orientacoes-manuais/manuais/manual-hidrowebservice_publica.pdf
- Swagger: https://www.ana.gov.br/hidrowebservice/swagger-ui/index.html
- SGB/SACE: https://sgb.gov.br/sace/
