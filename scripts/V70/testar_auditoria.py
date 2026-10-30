"""Teste sintético — NÃO contém dados reais de rios."""
import tempfile,json
from pathlib import Path
from auditar_json_ana import audit_file
with tempfile.TemporaryDirectory() as d:
    p=Path(d)/'ficticio.json'
    p.write_text(json.dumps({'status':'OK','items':[{'codigoestacao':'00000000','Data_Hora_Medicao':'2022-05-01 12:00:00.0','Cota_Adotada':'200','Cota_Adotada_Status':'0'},{'codigoestacao':'00000000','Data_Hora_Medicao':'2022-05-01 12:00:00.0','Cota_Adotada':None,'Cota_Adotada_Status':'1'}]}))
    rows,rep=audit_file(p)
    assert len(rows)==2 and rep['duplicidades_estacao_timestamp']==1
    assert rows[1]['cota_cm']=='' and rep['fuso_horario'].startswith('NÃO DETERMINADO')
print('TESTES OK: duplicidade detectada, valor ausente preservado, fuso não inferido.')
