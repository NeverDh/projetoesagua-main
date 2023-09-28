from flask import Flask, request
import threading
from importacoes import *
import auxiliar
import pandas as pd

app = Flask(__name__)

#DESENVOLVENDO WEBHOOK#
    
# def verificarProcessos():
#     schedule.every(1).seconds.do(enviarMensagem)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# def enviarMensagem():
#     print("Teste")

# def continuarProcessos():
#     contatos_processo = pd.read_excel("contatos_processo.xlsx")

def enviarNotificacao():
    None

def iniciarServer():
    app.run(port=7399)


@app.route("/chat", methods=['POST'])
def chat():
    try:
        verifica = request.json["Type"]
        thread = threading.Thread(target=auxiliar.mensagemRecebida, args=(request.json,))
        thread.start()
    except Exception as e:
        return "Não interessa"
    return "Concluído"


@app.route("/", methods=['POST'])
def index():
    return "ROBO EM FUNCIONAMENTO"

if __name__ == "__main__":
    y = threading.Thread(target=iniciarServer)
    y.start()
    objeto_automacao_planilha = planilhauto()
    objeto_automacao_planilha.automacao_planilha()
    auxiliar.integrarPlanilhas()

    