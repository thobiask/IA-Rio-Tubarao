from pathlib import Path
import pandas as pd, numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
out=Path('/mnt/data/Rio_Tubarao_V71_selecao_estacoes');out.mkdir(exist_ok=True)
p='/mnt/data/base_tratada_ia_com_metadados.csv'
d=pd.read_csv(p,usecols=['data','estacao_codigo','nivel_cm','nivel_cm_qualidade_estrita'],low_memory=False)
d['data']=pd.to_datetime(d['data'],errors='coerce');d['nivel_cm']=pd.to_numeric(d.nivel_cm,errors='coerce');d['ok']=d.nivel_cm_qualidade_estrita.astype(str).str.lower().eq('true') & d.nivel_cm.between(-200,3000)
d=d[d.ok].drop_duplicates(['data','estacao_codigo'],keep=False)
codes=[84580000,84300000,84560000,84559800,84249998]; names={84580000:'Rio do Pouso (Tubarão)',84300000:'Pedras Grandes',84560000:'São Ludgero',84559800:'Braço do Norte',84249998:'Orleans Montante'}
a=d[d.estacao_codigo.isin(codes)].pivot(index='data',columns='estacao_codigo',values='nivel_cm').sort_index();a=a.reindex(pd.date_range(a.index.min(),a.index.max(),freq='D'));a.index.name='data'
T=84580000; features=pd.DataFrame(index=a.index)
for lag in range(4):features[f'alvo_lag{lag}']=a[T].shift(lag)
features['alvo_delta1']=a[T]-a[T].shift(1);features['alvo_delta2']=a[T].shift(1)-a[T].shift(2)
for code in codes[1:]:
 for lag in range(2):features[f'{code}_lag{lag}']=a[code].shift(lag)
features['y']=a[T].shift(-1);features['nivel_atual']=a[T]
base_cols=[c for c in features if c.startswith('alvo_')];cand={code:[f'{code}_lag0',f'{code}_lag1'] for code in codes[1:]}
scenarios={'A_todas':codes[1:],'B_sem_pedras_grandes':[84560000,84559800,84249998],'C_sem_sao_ludgero':[84300000,84559800,84249998],'D_so_alvo':[]}
all_cols=base_cols+[c for cols in cand.values() for c in cols]+['y','nivel_atual']
common=features.dropna(subset=all_cols).copy(); common=common[(common.index>='1986-09-01')&(common.index<='2026-01-01')]
print('common',len(common),'years',common.index.min(),common.index.max()); print('splits',sum(common.index.year<=2015),sum((common.index.year>=2016)&(common.index.year<=2020)),sum((common.index.year>=2021)&(common.index.year<=2025)))
records=[]; predictions=[]; coverage=[]
for kind in ['fixo','disponibilidade']:
 for scenario,stations in scenarios.items():
  cols=base_cols+[c for code in stations for c in cand[code]]
  data=common if kind=='fixo' else features.dropna(subset=cols+['y','nivel_atual'])
  tr=data[data.index.year<=2015];val=data[(data.index.year>=2016)&(data.index.year<=2020)];te=data[(data.index.year>=2021)&(data.index.year<=2025)]
  coverage.append({'protocolo':kind,'cenario':scenario,'n_treino':len(tr),'n_validacao':len(val),'n_teste':len(te),'inicio_teste':str(te.index.min().date()) if len(te) else '', 'fim_teste':str(te.index.max().date()) if len(te) else ''})
  if min(len(tr),len(val),len(te))<20:continue
  model=make_pipeline(StandardScaler(),Ridge(alpha=10));model.fit(tr[cols],tr['y']);pred=model.predict(te[cols]);obs=te.y.to_numpy();persist=te.nivel_atual.to_numpy();rises=obs-persist
  for label,mask in [('todos',np.ones(len(te),bool)),('subidas_50cm',rises>=50),('subidas_100cm',rises>=100)]:
   if not mask.any():continue
   for method,values in [('ridge',pred),('persistencia',persist)]:
    records.append({'protocolo':kind,'cenario':scenario,'metodo':method,'recorte':label,'n':int(mask.sum()),'mae_cm':round(float(np.mean(abs(obs[mask]-values[mask]))),3),'rmse_cm':round(float(np.sqrt(np.mean((obs[mask]-values[mask])**2))),3)})
  if kind=='fixo':
   for date,y,p,base,rise in zip(te.index,obs,pred,persist,rises):predictions.append({'data_alvo':str((date+pd.Timedelta(days=1)).date()),'data_emissao':str(date.date()),'cenario':scenario,'observado_cm':y,'ridge_cm':p,'persistencia_cm':base,'subida_cm':rise})
pd.DataFrame(records).to_csv(out/'metricas_v71.csv',index=False);pd.DataFrame(coverage).to_csv(out/'cobertura_v71.csv',index=False);pd.DataFrame(predictions).to_csv(out/'previsoes_pareadas_v71.csv',index=False)
print(pd.DataFrame(coverage).to_string(index=False));print(pd.DataFrame(records).query("protocolo=='fixo' and metodo=='ridge'").to_string(index=False))
