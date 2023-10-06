import pandas as pd
from datetime import datetime, timedelta

now = datetime.now().strftime("%Y-%m-%d %H:%M")
now = datetime.strptime(now, "%Y-%m-%d %H:%M")

doisDias = now + timedelta(days=2)
umDia = now + timedelta(days=1)
seisHoras = now + timedelta(hours=6)
meiaHora = now + timedelta(minutes=30)
contatos_processo = pd.read_excel("contatos_processo.xlsx")
for index, data in enumerate(contatos_processo["Data"]):
    try:
        data = datetime.strptime(data, "%Y-%m-%d %H:%M")
        if umDia >= data:
            print(umDia, data) 
        if seisHoras >= data:
            print(seisHoras, data)
        if  meiaHora >= data:
            print(meiaHora, data)
    except Exception:
        None
    


            
