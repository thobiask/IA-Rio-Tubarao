from pathlib import Path
import pandas as pd, zipfile, hashlib, json
ROOT=Path('/mnt/data'); OUT=ROOT/'Rio_Tubarao_V69_diagnostico_e_aquisicao'; OUT.mkdir(exist_ok=True)
base=ROOT/'base_ia_hidrologia_chuvas_3_estacoes.csv'
cols=['data','estacao_codigo','nivel_cm','nivel_cm_qualidade_estrita','chuva_orleans_mm_dia','chuva_braco_do_norte_mm_dia','chuva_tubarao_mm_dia']
df=pd.read_csv(base,usecols=lambda c:c in cols,low_memory=False)
df['data']=pd.to_datetime(df['data'],errors='coerce')
df['estacao_codigo']=df['estacao_codigo'].astype('string')
jan=[('maio_2022','2022-04-27','2022-05-12'),('outubro_2023','2023-10-01','2023-10-25')]
focus=['84249998','84300000','84559800','84560000','84580000']
rows=[]
for name,ini,fim in jan:
 sub=df[df.data.between(ini,fim)]
 for cod in focus:
  g=sub[sub.estacao_codigo==cod]
  days=pd.date_range(ini,fim)
  valid=g[g.nivel_cm.notna()]
  strict=g[(g.nivel_cm.notna()) & (g.nivel_cm_qualidade_estrita.astype(str).str.lower().isin(['true','1']))]
  rows.append({'episodio':name,'codigo':cod,'dias_janela':len(days),'registros':len(g),'dias_com_nivel':valid.data.dt.normalize().nunique(),'dias_nivel_estrito':strict.data.dt.normalize().nunique(),'dias_sem_nivel':len(days)-valid.data.dt.normalize().nunique(),'datas_unicas':g.data.dt.normalize().nunique(),'timestamp_hora_distinta_na_base':g.data.dt.strftime('%H:%M:%S').nunique(),'possui_medicao_subdiaria_comprovada':False})
pd.DataFrame(rows).to_csv(OUT/'diagnostico_cobertura_eventos.csv',index=False)
# Validate rainfall separately: same daily rain repeated on each station's row, avoid treating as independent records.
rain=[]
for name,ini,fim in jan:
 g=df[df.data.between(ini,fim)]
 for c in [c for c in cols if c.startswith('chuva_')]:
  daily=g.groupby(g.data.dt.normalize())[c].agg(lambda s:s.dropna().iloc[0] if s.notna().any() else float('nan'))
  rain.append({'episodio':name,'variavel':c,'dias_janela':len(pd.date_range(ini,fim)),'dias_com_valor':int(daily.notna().sum()),'dias_sem_valor':len(pd.date_range(ini,fim))-int(daily.notna().sum())})
pd.DataFrame(rain).to_csv(OUT/'cobertura_chuva_eventos.csv',index=False)
# Raw rainfall archives are monthly ANA CSV, not demonstrated hourly records.
raw=[]
for p in sorted(ROOT.glob('Estacao_*zip')):
 with zipfile.ZipFile(p) as z:
  for x in z.infolist():
   if x.is_dir():continue
   raw.append({'arquivo':p.name,'conteudo':x.filename,'bytes_descompactados':x.file_size,'tipo':'chuva CSV ANA (granularidade por verificar; não comprovada horária)'})
pd.DataFrame(raw).to_csv(OUT/'inventario_arquivos_chuva.csv',index=False)
# Template acquisition: no claimed online availability
acq=[]
for cod,nome in [('84249998','Orleans — Montante'),('84300000','Pedras Grandes'),('84559800','Braço do Norte'),('84560000','São Ludgero'),('84580000','Tubarão — Rio do Pouso')]:
 for name,ini,fim in jan:
  acq.append({'estacao_codigo':cod,'rotulo_local':nome,'episodio':name,'inicio':ini,'fim':fim,'fonte_prioritaria':'ANA HidroWebService / inventário oficial','inventario_oficial_verificado':'NÃO','serie_subdiaria_disponivel':'NÃO VERIFICADO','timestamps_com_fuso':'PENDENTE','tipo_observacao':'PENDENTE','unidade_e_datum':'PENDENTE','arquivo_obtido':'','responsavel':'','observacoes':''})
pd.DataFrame(acq).to_csv(OUT/'plano_aquisicao_subdiaria.csv',index=False)
manifest={'base':base.name,'sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'fonte_auditoria_anterior':'Rio_Tubarao_V68_auditoria_eventos/RELATORIO_V68.md','natureza':'diagnostico local; sem coleta externa; sem treinamento'}
(OUT/'MANIFESTO.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
coverage=pd.read_csv(OUT/'diagnostico_cobertura_eventos.csv'); chuva=pd.read_csv(OUT/'cobertura_chuva_eventos.csv')
report=f'''# V69 — Diagnóstico de prontidão para séries subdiárias\n\n**Data:** 30/10/2026. **Escopo:** auditoria local e plano de aquisição; **não** foram obtidos dados horários novos, nem treinados novos modelos.\n\n## 1. Evidências disponíveis\n\n- Base consolidada: `{base.name}`; {len(df):,} registros; {df.estacao_codigo.nunique()} códigos de estação.\n- A coluna `data` é diária no conjunto consolidado; timestamps à meia-noite não demonstram observação à meia-noite.\n- Foram inspecionados {len(raw)} arquivos internos de {len(set(r['arquivo'] for r in raw))} ZIPs de chuva. A presença de CSV de chuva **não** comprova resolução horária.\n- A V68 já documentou ausências críticas de chuva em outubro/2023 e falhas em elevações de maio/2022.\n\n## 2. Cobertura de nível nos episódios (base local)\n\n{coverage[['episodio','codigo','dias_janela','dias_com_nivel','dias_nivel_estrito','dias_sem_nivel']].to_markdown(index=False)}\n\n**Nota:** o filtro estrito foi inferido da coluna `nivel_cm_qualidade_estrita`; a V68 é a referência para pares de previsão elegíveis. Contagem de dias não equivale a avaliação de acertos de alerta.\n\n## 3. Cobertura de chuva diária\n\n{chuva.to_markdown(index=False)}\n\nA ausência de valor é lacuna de observação, não chuva zero. Mesmo chuva diária presente pode não estar disponível no instante de emissão da previsão.\n\n## 4. Resultados da auditoria V68 a preservar\n\n- Maio/2022: 61 pares elegíveis para subida ≥50 cm, 12 subidas reais elegíveis, 6 detectadas e 13 falsos positivos.\n- Outubro/2023: Braço do Norte, 25 pares elegíveis, 4 subidas, 2 detectadas e 12 falsos positivos; Rio do Pouso, 7 pares elegíveis, 2 subidas, 0 detectadas.\n- Elevações de um dia para outro **não** informam a hora da subida, tempo de propagação ou antecedência de alerta.\n\n## 5. O que precisa ser obtido antes do próximo treinamento\n\n1. **Inventário oficial ANA:** confirmar código, nome, localização, datum, tipo de medição e operação das cinco estações.\n2. **Séries subdiárias:** consultar ANA HidroWebService (telemetria adotada/detalhada), SGB e fontes locais, sem presumir disponibilidade.\n3. **Chuva:** verificar CEMADEN, Defesa Civil e telemetria ANA, documentando cobertura e latência.\n4. **Metadados obrigatórios:** `estacao_codigo`, `timestamp_original`, `fuso`, `timestamp_utc`, `variavel`, `valor`, `unidade`, `status_qualidade`, `fonte`, `data_extracao`, `tipo_tempo` (observação/transmissão).\n5. **Critérios de aceite:** cobertura em maio/2022 e outubro/2023; ausência de duplicidades conflitantes; intervalos efetivos medidos; fuso validado; não interpolar lacunas críticas; comparações de nível apenas com referência local de régua.\n\n**Fontes técnicas já identificadas na V63:** https://www.ana.gov.br/hidrowebservice/swagger-ui/index.html e manual em https://www.gov.br/ana/pt-br/assuntos/monitoramento-e-eventos-criticos/monitoramento-hidrologico/orientacoes-manuais/manuais/manual-hidrowebservice_publica.pdf . A API pode requerer cadastro e credenciais.\n\n## 6. Plano experimental após aquisição\n\n- Comparar horizontes de **3, 6, 12 e 24 horas**, apenas nas estações com séries realmente adequadas.\n- Baselines: persistência, Ridge, Random Forest, Gradient Boosting; MLP como hipótese adicional.\n- Divisão temporal sem vazamento; validação por eventos independentes; registrar MAE/RMSE, recall, precisão, falsos alarmes e antecedência.\n- Não chamar subida de ≥50 cm de enchente sem rótulos de impactos ou limiares oficiais validados.\n\n## 7. Próxima ação operacional\n\nPreencher `plano_aquisicao_subdiaria.csv` com consulta oficial por código e janela; salvar arquivos brutos imutáveis, metadados e comprovantes de origem. Somente então iniciar V70 (comparação com dados subdiários).\n\n## 8. Arquivos gerados\n\n- `diagnostico_cobertura_eventos.csv` — nível por estação e janela.\n- `cobertura_chuva_eventos.csv` — cobertura diária por variável.\n- `inventario_arquivos_chuva.csv` — arquivos locais de chuva.\n- `plano_aquisicao_subdiaria.csv` — checklist operacional.\n- `MANIFESTO.json` — integridade da base consolidada.\n'''
(OUT/'RELATORIO_V69.md').write_text(report,encoding='utf-8')
with zipfile.ZipFile(ROOT/'Rio_Tubarao_V69_pacote.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in OUT.iterdir():z.write(f,arcname=f.name)
print('REGISTROS',len(df),'ESTACOES',df.estacao_codigo.nunique(),'ZIP', (ROOT/'Rio_Tubarao_V69_pacote.zip').stat().st_size)
print(coverage[['episodio','codigo','dias_com_nivel','dias_nivel_estrito']].to_string(index=False))
print(chuva.to_string(index=False))
