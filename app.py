from flask import Flask, request
import threading
from importacoes import *
import auxiliar
import schedule
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)

#DESENVOLVENDO WEBHOOK#

def enviarNotificacao():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    now = datetime.strptime(now, "%Y-%m-%d %H:%M")

    doisDias = now + timedelta(days=2)
    umDia = now + timedelta(days=1)
    umaHora = now + timedelta(hours=1)
    meiaHora = now + timedelta(minutes=30)
    contatos_processo = pd.read_excel("contatos_processo.xlsx")

    for index, data in enumerate(contatos_processo["Data"]):
        notificar = False
        processoNotificacao = 0
        codMovel = contatos_processo["codImovel"][index]
        data = datetime.strptime(data, "%Y-%m-%d %H:%M")
        if doisDias >= data or umDia >= data or umaHora >= data or meiaHora >= data:
            notificar = True

        if doisDias >= data:
            processoNotificacao = 1
        if umDia >= data:
            processoNotificacao = 2
        if umaHora >= data:
            processoNotificacao = 3
        if meiaHora >= data:
            processoNotificacao = 4

        if notificar == True:
            match processoNotificacao:
                case 1:
                    auxiliar.enviarMensagem(f'Você confirma a visitação ao imóvel: {codMovel} no dia {data}?\n1 - Sim\n2 - Não', "?")
                case 2:
                    auxiliar.enviarMensagem(f'Você confirma a visitação ao imóvel: {codMovel} no dia {data}?\n1 - Sim\n2 - Não', "?")
                case 3:
                    auxiliar.enviarMensagem(f'Você confirma a visitação ao imóvel: {codMovel} no dia {data}?\n1 - Sim\n2 - Não', "?")
                case 4:
                    auxiliar.enviarMensagem(f'Você confirma a visitação ao imóvel: {codMovel} no dia {data}?\n1 - Sim\n2 - Não', "?")


def exportarContatos():
    objeto_exportar = exportar()
    objeto_exportar.exportacao_contatos()

def integrarPlanilhas():
    objeto_automacao_planilha = planilhauto()
    objeto_automacao_planilha.automacao_planilha()
    auxiliar.integrarPlanilhas()
    
def verificarProcessos():
    while True:
        schedule.run_pending()
        time.sleep(300)

def iniciarServer():
    app.run(port=5000)


@app.route("/chat", methods=['POST'])
def chat():
    try:
        verifica = request.json
        if verifica["Type"] == "receveid_message":
            numero = (verifica["Body"]["Info"]["RemoteJid"])[4:13]
            processoIndex = auxiliar.verificarProcesso(numero)
            if processoIndex != None:
                thread = threading.Thread(target=auxiliar.mensagemRecebida, args=(request.json,))
                thread.daemon = True
                thread.start()
            else:
                return "Não interessa"
    except Exception as e:
        return "Não interessa"
    return "Concluído"


@app.route("/", methods=['POST'])
def index():
    return "ROBO EM FUNCIONAMENTO"

if __name__ == "__main__":
    schedule.every(60).minutes.do(exportarContatos)
    schedule.every(70).minutes.do(integrarPlanilhas)
    schedule.every(30).minutes.do(enviarNotificacao)
    y = threading.Thread(target=verificarProcessos)
    y.start()
    iniciarServer()
    