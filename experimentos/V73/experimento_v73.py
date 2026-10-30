from pathlib import Path
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import precision_score,recall_score,f1_score,fbeta_score,confusion_matrix,average_precision_score,roc_auc_score
ROOT=Path(__file__).resolve().parent/'Rio_Tubarao_V73_classificacao';ROOT.mkdir(exist_ok=True)
SOURCE=Path('/mnt/data/base_tratada_ia_com_metadados.csv')
CODES=[84580000,84300000,84560000,84559800,84249998];TARGET=CODES[0]
d=pd.read_csv(SOURCE,usecols=['data','estacao_codigo','nivel_cm','nivel_cm_qualidade_estrita'],low_memory=False)
d['data']=pd.to_datetime(d.data,errors='coerce');d['nivel_cm']=pd.to_numeric(d.nivel_cm,errors='coerce');d['ok']=d.nivel_cm_qualidade_estrita.astype(str).str.lower().eq('true')&d.nivel_cm.between(-200,3000)
d=d[d.ok].drop_duplicates(['data','estacao_codigo'],keep=False)
a=d[d.estacao_codigo.isin(CODES)].pivot(index='data',columns='estacao_codigo',values='nivel_cm').sort_index();a=a.reindex(pd.date_range(a.index.min(),a.index.max(),freq='D'));a.index.name='data'
f=pd.DataFrame(index=a.index)
for lag in range(4):f[f'alvo_lag{lag}']=a[TARGET].shift(lag)
f['alvo_delta1']=a[TARGET]-a[TARGET].shift(1);f['alvo_delta2']=a[TARGET].shift(1)-a[TARGET].shift(2)
base_cols=list(f.columns);aux_cols=[]
for code in CODES[1:]:
 for lag in range(2):
  c=f'{code}_lag{lag}';f[c]=a[code].shift(lag);aux_cols.append(c)
f['y_prox']=a[TARGET].shift(-1);f['nivel_atual']=a[TARGET]
data=f.dropna(subset=base_cols+['y_prox','nivel_atual']).copy();data=data[(data.index>='1986-09-01')&(data.index<='2026-01-01')]
for c in aux_cols:data[c+'_presente']=data[c].notna().astype(float)
cols=base_cols+aux_cols+[c+'_presente' for c in aux_cols]
tr=data[data.index.year<=2015];val=data[(data.index.year>=2016)&(data.index.year<=2020)];te=data[(data.index.year>=2021)&(data.index.year<=2025)]

def metrics(y,p):
 tn,fp,fn,tp=confusion_matrix(y,p,labels=[0,1]).ravel()
 return dict(tp=int(tp),fp=int(fp),fn=int(fn),tn=int(tn),precisao=round(float(precision_score(y,p,zero_division=0)),4),recall=round(float(recall_score(y,p,zero_division=0)),4),f1=round(float(f1_score(y,p,zero_division=0)),4),f2=round(float(fbeta_score(y,p,beta=2,zero_division=0)),4),alertas=int(p.sum()))
rows=[];preds=[];threshold_rows=[]
for rise in [50,100]:
 ytr=((tr.y_prox-tr.nivel_atual)>=rise).astype(int);yv=((val.y_prox-val.nivel_atual)>=rise).astype(int);yt=((te.y_prox-te.nivel_atual)>=rise).astype(int)
 models={
  'regressao_logistica':make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),LogisticRegression(class_weight='balanced',max_iter=1000,random_state=42)),
  'hist_gradient_boosting':HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=15,min_samples_leaf=30,l2_regularization=10,learning_rate=.05,random_state=42),
 }
 for name,model in models.items():
  model.fit(tr[cols],ytr);pv=model.predict_proba(val[cols])[:,1];pt=model.predict_proba(te[cols])[:,1]
  # Threshold optimized on validation only. Include zero-alert solution only if all F2 are zero.
  candidates=np.arange(.05,.951,.025)
  scored=[]
  for t in candidates:
   met=metrics(yv,(pv>=t).astype(int));scored.append((met['f2'],met['precisao'],-met['fp'],float(t),met))
  best=max(scored,key=lambda x:(x[0],x[1],x[2],x[3]));threshold=best[3]
  threshold_rows.append(dict(limiar_subida_cm=rise,modelo=name,limiar_probabilidade=threshold,n_validacao=len(val),eventos_validacao=int(yv.sum()),**{'valid_'+k:v for k,v in best[4].items()}))
  for cutoff_name,cutoff in [('fixo_050',.5),('ajustado_validacao',threshold)]:
   yp=(pt>=cutoff).astype(int);met=metrics(yt,yp)
   rows.append(dict(limiar_subida_cm=rise,modelo=name,regra=cutoff_name,limiar_probabilidade=round(float(cutoff),4),n_teste=len(te),eventos_teste=int(yt.sum()),taxa_base=round(float(yt.mean()),4),average_precision=round(float(average_precision_score(yt,pt)),4),**met))
   for date,real,prob,pred in zip(te.index,yt,pt,yp):
    preds.append(dict(data_emissao=date.date().isoformat(),data_alvo=(date+pd.Timedelta(days=1)).date().isoformat(),limiar_subida_cm=rise,modelo=name,regra=cutoff_name,probabilidade=round(float(prob),6),observado_evento=int(real),alerta=int(pred),subida_real_cm=float(te.loc[date,'y_prox']-te.loc[date,'nivel_atual'])))
 # Baseline no alert, last-day-rise threshold (requires current and previous observed)
 for name,yp in [('sem_alerta',np.zeros(len(te),dtype=int)),('repetir_subida_anterior',(te.alvo_delta1>=rise).astype(int).to_numpy())]:
  rows.append(dict(limiar_subida_cm=rise,modelo=name,regra='regra_fixa',limiar_probabilidade=np.nan,n_teste=len(te),eventos_teste=int(yt.sum()),taxa_base=round(float(yt.mean()),4),average_precision=np.nan,**metrics(yt,yp)))
  for date,real,pred in zip(te.index,yt,yp):
   preds.append(dict(data_emissao=date.date().isoformat(),data_alvo=(date+pd.Timedelta(days=1)).date().isoformat(),limiar_subida_cm=rise,modelo=name,regra='regra_fixa',probabilidade=np.nan,observado_evento=int(real),alerta=int(pred),subida_real_cm=float(te.loc[date,'y_prox']-te.loc[date,'nivel_atual'])))
pd.DataFrame(rows).to_csv(ROOT/'metricas_v73.csv',index=False);pd.DataFrame(threshold_rows).to_csv(ROOT/'limiares_validacao_v73.csv',index=False);pd.DataFrame(preds).to_csv(ROOT/'previsoes_v73.csv',index=False)
print('coortes',len(tr),len(val),len(te));print(pd.DataFrame(rows).to_string(index=False));print('limiares',pd.DataFrame(threshold_rows).to_string(index=False))
