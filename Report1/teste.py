from datetime import datetime
from datetime import timedelta  
from datetime import time
import datetime as dt

import re

records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564627800, 'start': 1564626000}
]


def classify_by_phone_number(records):
    consolidado = {}
    
    for r in records:
        if r['source'] not in consolidado:
            consolidado[r['source']] = 0 
        
        dt_ini = datetime.fromtimestamp(r['start'])
        dt_fim = datetime.fromtimestamp(r['end'])

        delta = dt_fim - dt_ini

        min_charged = 0
        for minute in range(1, delta.seconds // 60 + 1):
            horario_usado = dt_ini + timedelta(minutes=1)
            horario_usado = horario_usado.time()

            if (horario_usado >= dt.time(6,0) and horario_usado < dt.time(22,0)):
                min_charged += 1


        consolidado[r['source']] += 0.36 + min_charged * 0.09

    sorted_d = dict(sorted(consolidado.items(), key=operator.itemgetter(1),reverse=True))

    
    import operator

    for key in dict(sorted(consolidado.items(), key=operator.itemgetter(1),reverse=True)) :
        lista_dados_final.append({'source' : key, 'total' : consolidado[key]})

    # return lista_dados_final

    return None

teste = classify_by_phone_number(records)

print(teste)