import pandas as pd
from datetime import datetime, timedelta
import auxiliar

now = datetime.now().strftime("%Y-%m-%d %H:%M")
now = datetime.strptime(now, "%Y-%m-%d %H:%M")

doisDias = now + timedelta(days=2)
umDia = now + timedelta(days=1)
seisHoras = now + timedelta(hours=6)
meiaHora = now + timedelta(minutes=30)
contatos_processo = pd.read_excel("contatos_processo.xlsx")
for _, data in enumerate(contatos_processo["Data"]):
    notificar = False
    data = datetime.strptime(data, "%Y-%m-%d %H:%M")
    if doisDias >= data or umDia >= data or seisHoras >= data or meiaHora >= data:
        notificar = True
    if notificar == True:
        auxiliar.enviarMensagem(f'Você confirma a visitação ao imóvel: {None} no dia {data}', "?")
    


            
