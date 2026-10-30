import pandas as pd, numpy as np, shutil, zipfile
from pathlib import Path
p=Path('/mnt/data/Rio_Tubarao_V71_selecao_estacoes'); pred=pd.read_csv(p/'previsoes_pareadas_v71.csv'); pred['data_emissao']=pd.to_datetime(pred.data_emissao);pred['mes']=pred.data_emissao.dt.to_period('M').astype(str)
wide=pred.pivot(index='data_emissao',columns='cenario',values='ridge_cm'); ref=pred[pred.cenario=='A_todas'].set_index('data_emissao'); months=ref['mes'].unique(); rng=np.random.default_rng(71);rows=[]
for scen in ['B_sem_pedras_grandes','C_sem_sao_ludgero','D_so_alvo']:
 for recorte,mask in [('todos',np.ones(len(ref),bool)),('subidas_50cm',ref.subida_cm.to_numpy()>=50)]:
  dif=np.abs(wide[scen].to_numpy()-ref.observado_cm.to_numpy())-np.abs(wide['A_todas'].to_numpy()-ref.observado_cm.to_numpy())
  val=float(dif[mask].mean()); draws=[]
  montharr=ref.mes.to_numpy()
  for _ in range(2000):
   sampled=rng.choice(months,size=len(months),replace=True);idx=np.concatenate([np.where(montharr==m)[0] for m in sampled]);idx=idx[mask[idx]]
   if len(idx):draws.append(float(dif[idx].mean()))
  low,high=np.percentile(draws,[2.5,97.5])
  rows.append({'cenario':scen,'recorte':recorte,'n':int(mask.sum()),'delta_mae_vs_todas_cm':round(val,3),'ic95_bootstrap_mensal_inf':round(low,3),'ic95_bootstrap_mensal_sup':round(high,3),'reamostragens_validas':len(draws)})
pd.DataFrame(rows).to_csv(p/'diferencas_bootstrap_v71.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))
report='''# V71 — Seleção de estações: ablação pareada para previsão do Rio do Pouso

**Data:** 30/10/2026. **Natureza:** experimento exploratório local, sem novos dados da ANA.\n
## Pergunta
A exclusão de estações com cobertura inferior melhora a previsão diária da cota da estação 84580000 (Rio do Pouso, Tubarão)?

## Fonte e protocolo
- Fonte: `base_tratada_ia_com_metadados.csv` (base local ANA consolidada). Estação 84580000 consta erroneamente como Orleans no arquivo de origem; V64 corrigiu documentalmente para Rio do Pouso, Tubarão.
- Alvo: nível do dia seguinte, em centímetros, na estação 84580000. **Não equivale a alerta de enchente**.
- Cinco estações: alvo 84580000; candidatas 84300000 (Pedras Grandes), 84560000 (São Ludgero), 84559800 (Braço do Norte), 84249998 (Orleans-Montante).
- Registros: somente `nivel_cm_qualidade_estrita=True`, valores entre -200 e 3000 cm, datas diárias exatas, sem interpolação. Registros duplicados por código/data excluídos para evitar ambiguidade.
- Entradas do alvo: nível em D, D-1, D-2, D-3 e duas diferenças anteriores; cada estação auxiliar contribui nível em D e D-1. Alvo é D+1.
- Modelo: `StandardScaler` + `Ridge(alpha=10)`; sem otimização no teste. Baseline: persistência (nível D).
- Treino até 2015; validação 2016–2020; teste 2021–2025, respeitando dados elegíveis.
- **Comparação principal de ablação com coorte fixa**: exige disponibilidade das quatro estações auxiliares em D e D-1, mesmo quando excluídas da configuração. Isto preserva exatamente as mesmas datas de treino e teste para todas as variantes. A comparação mede contribuição preditiva, **não** o ganho de cobertura por retirar uma estação.
- Segunda comparação `disponibilidade`: cada variante usa todas as suas datas elegíveis; números **não são comparáveis diretamente** entre configurações devido à mudança de datas e treino.

## Cobertura da coorte fixa
Treino: **2953** dias; validação: **557**; teste: **221**, entre 2021-01-01 e 2023-06-16. A análise **não cobre outubro de 2023**, apesar de o período nominal de teste chegar a 2025.

## Resultados principais: coorte fixa
| Cenário | MAE todos (cm) | MAE subidas ≥50 cm (cm), n=10 | MAE subidas ≥100 cm (cm), n=5 |
|---|---:|---:|---:|
| Todas | 21,075 | 104,272 | 126,240 |
| Sem Pedras Grandes | 21,881 | 100,554 | 121,600 |
| Sem São Ludgero | 23,247 | 98,587 | 120,293 |
| Só Rio do Pouso | 24,848 | 104,586 | 133,871 |
| Persistência | 25,448 | 105,000 | 134,800 |

**Interpretação:** remover Pedras Grandes ou São Ludgero **piora o MAE global** nesta coorte fixa, embora os erros condicionais em dez subidas de ≥50 cm fiquem menores. O tamanho de amostra extremo é insuficiente para afirmar ganho robusto ou eficácia operacional. Não confundir erros em dias com subidas observadas com detecção de eventos em tempo real.

## Disponibilidade quando retiramos estações
- Todas: 221 dias de teste.
- Sem Pedras Grandes: 311 dias de teste.
- Sem São Ludgero: 223 dias de teste.
- Só Rio do Pouso: 933 dias de teste, até 2023-11-18.

Essas amostras diferem; não comparar seus MAEs como se fossem o mesmo conjunto de dias. Excluir estação auxiliar pode recuperar dias utilizáveis, mas também retirar informação preditiva.

## Limitações
1. Estações podem não estar fisicamente conectadas como suposto; metadados e horas reais de leitura não foram revalidados nesta etapa.
2. Apenas Ridge foi retreinado; resultados não demonstram que a exclusão prejudique ou ajude Random Forest, Gradient Boosting ou MLP.
3. Coorte fixa tem somente 221 dias de teste e dez elevações ≥50 cm; o recorte de eventos extremos é frágil.
4. O uso de medições em D pressupõe disponibilidade no instante da previsão; não foi auditado o horário real.
5. A ausência de chuva e a resolução diária continuam limitando a análise.
6. Critério de qualidade estrita não garante ausência de erros hidrológicos; comparar com séries brutas e inventário oficial.
7. Não foram realizadas seleções de variáveis com base no teste para estabelecer um modelo final; cenários são **hipóteses exploratórias**, não decisão definitiva.

## Decisão
**Não excluir definitivamente Pedras Grandes nem São Ludgero.** Manter todas as estações no repositório, mas considerar modelos tolerantes a valores ausentes, máscaras de disponibilidade e comparação em janelas fixas, além de séries horárias. A hipótese de que retirar a pior cobertura aumenta a precisão global **não se confirmou neste teste Ridge**.

## Reproduzir
`python run_v71.py` (ajustar os caminhos de entrada e saída no início do arquivo). Dependências: pandas, numpy, scikit-learn. `finalizar_v71.py` calcula as diferenças e intervalos exploratórios por bootstrap mensal e escreve este relatório.
'''
report+='\n## Incerteza exploratória das diferenças de MAE (exclusão menos todas)\n\n'+pd.DataFrame(rows).to_markdown(index=False)+'\n\nValores negativos favorecem a exclusão. Bootstrap mensal de 2.000 reamostragens, com somente 10 eventos extremos no teste; intervalos são indicativos, não conclusivos.\n'
(p/'RELATORIO_V71.md').write_text(report,encoding='utf-8')
shutil.copy('/mnt/data/run_v71.py',p/'run_v71.py');shutil.copy('/mnt/data/finalizar_v71.py',p/'finalizar_v71.py')
zipname=Path('/mnt/data/Rio_Tubarao_V71_pacote.zip')
with zipfile.ZipFile(zipname,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for f in p.iterdir():
  if f.is_file():z.write(f,arcname=f.name)
print('ZIP',zipname,zipname.stat().st_size)
