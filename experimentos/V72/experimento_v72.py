from pathlib import Path
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor

ROOT=Path(__file__).resolve().parent
SOURCE=Path('/mnt/data/base_tratada_ia_com_metadados.csv')
CODES=[84580000,84300000,84560000,84559800,84249998]
TARGET=CODES[0]
d=pd.read_csv(SOURCE,usecols=['data','estacao_codigo','nivel_cm','nivel_cm_qualidade_estrita'],low_memory=False)
d['data']=pd.to_datetime(d['data'],errors='coerce')
d['nivel_cm']=pd.to_numeric(d['nivel_cm'],errors='coerce')
d['ok']=d.nivel_cm_qualidade_estrita.astype(str).str.lower().eq('true') & d.nivel_cm.between(-200,3000)
d=d[d.ok].drop_duplicates(['data','estacao_codigo'],keep=False)
a=d[d.estacao_codigo.isin(CODES)].pivot(index='data',columns='estacao_codigo',values='nivel_cm').sort_index()
a=a.reindex(pd.date_range(a.index.min(),a.index.max(),freq='D'));a.index.name='data'
f=pd.DataFrame(index=a.index)
for lag in range(4):f[f'alvo_lag{lag}']=a[TARGET].shift(lag)
f['alvo_delta1']=a[TARGET]-a[TARGET].shift(1)
f['alvo_delta2']=a[TARGET].shift(1)-a[TARGET].shift(2)
base_cols=list(f.columns)
aux_cols=[]
for code in CODES[1:]:
 for lag in range(2):
  c=f'{code}_lag{lag}';f[c]=a[code].shift(lag);aux_cols.append(c)
f['y']=a[TARGET].shift(-1)
f['nivel_atual']=a[TARGET]
# Target features and next-day observation must be available, auxiliaries may be missing.
data=f.dropna(subset=base_cols+['y','nivel_atual']).copy()
data=data[(data.index>='1986-09-01')&(data.index<='2026-01-01')]
tr=data[data.index.year<=2015].copy()
val=data[(data.index.year>=2016)&(data.index.year<=2020)].copy()
te=data[(data.index.year>=2021)&(data.index.year<=2025)].copy()
# Explicit availability flags; do not use future values or fill missing with zero.
for c in aux_cols:
 for part in [tr,val,te]:part.loc[:,c+'_presente']=part[c].notna().astype('float64')
flags=[c+'_presente' for c in aux_cols]
models={
 'ridge_alvo':(base_cols,make_pipeline(StandardScaler(),Ridge(alpha=10))),
 'ridge_multifonte_faltantes':(base_cols+aux_cols+flags,make_pipeline(SimpleImputer(strategy='median',add_indicator=False),StandardScaler(),Ridge(alpha=10))),
 'hgb_multifonte_faltantes':(base_cols+aux_cols+flags,HistGradientBoostingRegressor(max_iter=150,max_leaf_nodes=15,l2_regularization=10,learning_rate=.05,min_samples_leaf=30,random_state=42)),
}
preds=[]
for name,(cols,model) in models.items():
 model.fit(tr[cols],tr.y)
 pred=model.predict(te[cols])
 for date,y,p,persist in zip(te.index,te.y,pred,te.nivel_atual):
  preds.append({'data_emissao':str(date.date()),'data_alvo':str((date+pd.Timedelta(days=1)).date()),'modelo':name,'observado_cm':y,'previsto_cm':p,'persistencia_cm':persist,'subida_cm':y-persist,'n_aux_disponiveis':int(te.loc[date,aux_cols].notna().sum())})
# Ridge complete-case: train only when every auxiliary is present; compare on same full evaluation dates with all models.
complete_train=tr.dropna(subset=aux_cols);complete_test=te.dropna(subset=aux_cols)
model=make_pipeline(StandardScaler(),Ridge(alpha=10)).fit(complete_train[base_cols+aux_cols],complete_train.y)
for date,y,p,persist in zip(complete_test.index,complete_test.y,model.predict(complete_test[base_cols+aux_cols]),complete_test.nivel_atual):
 preds.append({'data_emissao':str(date.date()),'data_alvo':str((date+pd.Timedelta(days=1)).date()),'modelo':'ridge_casos_completos_v71','observado_cm':y,'previsto_cm':p,'persistencia_cm':persist,'subida_cm':y-persist,'n_aux_disponiveis':8})
p=pd.DataFrame(preds)
# one baseline on all target eligible days
base=pd.DataFrame({'data_emissao':te.index.strftime('%Y-%m-%d'),'data_alvo':(te.index+pd.Timedelta(days=1)).strftime('%Y-%m-%d'),'modelo':'persistencia','observado_cm':te.y.to_numpy(),'previsto_cm':te.nivel_atual.to_numpy(),'persistencia_cm':te.nivel_atual.to_numpy(),'subida_cm':(te.y-te.nivel_atual).to_numpy(),'n_aux_disponiveis':te[aux_cols].notna().sum(axis=1).to_numpy()})
p=pd.concat([p,base],ignore_index=True)
p.to_csv(ROOT/'previsoes_v72.csv',index=False)
rows=[]
for cohort,dates in [('todos_alvo',set(te.index.strftime('%Y-%m-%d'))),('coorte_completa',set(complete_test.index.strftime('%Y-%m-%d'))),('sem_todas_auxiliares',set(te.index.strftime('%Y-%m-%d'))-set(complete_test.index.strftime('%Y-%m-%d')))]:
 for name,g in p[p.data_emissao.isin(dates)].groupby('modelo'):
  for cut,sub in [('todos',g),('subidas_50cm',g[g.subida_cm>=50]),('subidas_100cm',g[g.subida_cm>=100])]:
   if len(sub)==0:continue
   err=sub.observado_cm-sub.previsto_cm
   rows.append({'coorte':cohort,'modelo':name,'recorte':cut,'n':len(sub),'mae_cm':round(float(err.abs().mean()),3),'rmse_cm':round(float(np.sqrt(np.mean(err**2))),3),'primeiro_dia':sub.data_emissao.min(),'ultimo_dia':sub.data_emissao.max()})
res=pd.DataFrame(rows);res.to_csv(ROOT/'metricas_v72.csv',index=False)
coverage=pd.DataFrame([{'coorte':'treino','n_alvo':len(tr),'n_completos':len(complete_train)},{'coorte':'validacao','n_alvo':len(val),'n_completos':int(val[aux_cols].notna().all(axis=1).sum())},{'coorte':'teste','n_alvo':len(te),'n_completos':len(complete_test)}]);coverage.to_csv(ROOT/'cobertura_v72.csv',index=False)
print(coverage.to_string(index=False));print(res[res.recorte.eq('todos')].to_string(index=False));print('subidas');print(res[res.recorte.eq('subidas_50cm')].to_string(index=False))
