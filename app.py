from flask import Flask, request
import threading
from importacoes import *
import auxiliar
import schedule

app = Flask(__name__)

#DESENVOLVENDO WEBHOOK#

def exportarContatos():
    objeto_exportar = exportar()
    objeto_exportar.exportacao_contatos()

def integrarPlanilhas():
    objeto_automacao_planilha = planilhauto()
    objeto_automacao_planilha.automacao_planilha()
    auxiliar.integrarPlanilhas()

def enviarNotificacao():
    None

    
def verificarProcessos():
    schedule.every(60).minutes.do(exportarContatos)
    schedule.every(70).minutes.do(integrarPlanilhas)
    while True:
        schedule.run_pending()
        time.sleep(1)

def iniciarServer():
    app.run(port=5000)


@app.route("/chat", methods=['POST'])
def chat():
    try:
        verifica = request.json
        if verifica["Type"] == "receveid_message":
            numero = (verifica["Body"]["Info"]["RemoteJid"])[4:13]
            processoIndex = auxiliar.verificarProcesso(numero)
            print(processoIndex)
            if processoIndex != None:
                thread = threading.Thread(target=auxiliar.mensagemRecebida, args=(request.json,))
                thread.start()
    except Exception as e:
        return "Não interessa"
    return "Concluído"


@app.route("/", methods=['POST'])
def index():
    return "ROBO EM FUNCIONAMENTO"

if __name__ == "__main__":
    y = threading.Thread(target=integrarPlanilhas)
    y.start()
    iniciarServer()
    