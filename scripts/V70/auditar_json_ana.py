#!/usr/bin/env python3
"""Auditoria conservadora de respostas JSON oficiais ANA HidroWebService.
Uso: python auditar_json_ana.py brutos --saida saidas
Não presume fuso, não inventa dados e não interpola valores ausentes.
"""
import argparse, csv, json, hashlib
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

FIELDS=['arquivo','codigo_estacao','timestamp_original','timestamp_atualizacao','cota_cm','cota_status','chuva_mm','chuva_status','vazao_m3_s','vazao_status','sha256_json']

def read_items(obj):
    if isinstance(obj,list): return obj
    if not isinstance(obj,dict): raise ValueError('JSON raiz não é objeto ou lista')
    if str(obj.get('status','OK')).upper() not in ('OK','SUCESSO'): raise ValueError('Status de API não OK: '+str(obj.get('status')))
    items=obj.get('items',None)
    if items is None: raise ValueError('Chave items ausente: inspecionar resposta')
    if isinstance(items,dict): items=[items]
    if not isinstance(items,list): raise ValueError('items não é lista')
    return items

def textval(item, key):
    v=item.get(key)
    return '' if v is None else str(v)

def audit_file(p):
    raw=p.read_bytes(); h=hashlib.sha256(raw).hexdigest()
    items=read_items(json.loads(raw.decode('utf-8-sig')))
    rows=[]; bad=0
    for item in items:
        if not isinstance(item,dict): bad+=1;continue
        rows.append({'arquivo':p.name,'codigo_estacao':textval(item,'codigoestacao'),
            'timestamp_original':textval(item,'Data_Hora_Medicao'),
            'timestamp_atualizacao':textval(item,'Data_Atualizacao'),
            'cota_cm':textval(item,'Cota_Adotada'),'cota_status':textval(item,'Cota_Adotada_Status'),
            'chuva_mm':textval(item,'Chuva_Adotada'),'chuva_status':textval(item,'Chuva_Adotada_Status'),
            'vazao_m3_s':textval(item,'Vazao_Adotada'),'vazao_status':textval(item,'Vazao_Adotada_Status'),
            'sha256_json':h})
    stamps=[r['timestamp_original'] for r in rows if r['timestamp_original']]
    counts=Counter((r['codigo_estacao'],r['timestamp_original']) for r in rows if r['timestamp_original'])
    duplicates=sum(v-1 for v in counts.values() if v>1)
    quality=Counter(r['cota_status'] or 'AUSENTE' for r in rows)
    return rows,{'arquivo':p.name,'registros':len(rows),'itens_invalidos':bad,
        'timestamps_ausentes':len(rows)-len(stamps),'timestamps_distintos':len(set(stamps)),
        'duplicidades_estacao_timestamp':duplicates,'cota_status_contagem':dict(quality),
        'sha256_json':h,'fuso_horario':'NÃO DETERMINADO — requer confirmação oficial',
        'serie_subdiaria_confirmada':False}

def main():
    a=argparse.ArgumentParser();a.add_argument('entrada',type=Path);a.add_argument('--saida',type=Path,default=Path('saidas'));args=a.parse_args()
    args.saida.mkdir(parents=True,exist_ok=True)
    paths=sorted(args.entrada.glob('*.json')) if args.entrada.is_dir() else [args.entrada]
    reports=[];allrows=[]
    for p in paths:
        try:
            rows,rep=audit_file(p);reports.append(rep);allrows+=rows
        except Exception as exc:reports.append({'arquivo':p.name,'erro':str(exc)})
    with (args.saida/'registros_ana_sem_fuso_inferido.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(allrows)
    (args.saida/'auditoria_json.json').write_text(json.dumps({'arquivos_processados':len(paths),'registros_extraidos':len(allrows),'resultados':reports,'alerta':'Não inferir fuso, qualidade, nem disponibilidade de dados por ausência de resposta.'},ensure_ascii=False,indent=2),encoding='utf-8')
    print('Arquivos:',len(paths),'Registros:',len(allrows),'Erros:',sum('erro' in x for x in reports))
    print('Saída:',args.saida)

if __name__=='__main__':main()
