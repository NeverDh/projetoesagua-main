from flask import Flask, request
import json
import schedule
import time
import threading
from importacoes import *
import auxiliar

app = Flask(__name__)

#DESENVOLVENDO WEBHOOK#
    
# def verificarProcessos():
#     schedule.every(1).seconds.do(enviarMensagem)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# def enviarMensagem():
#     print("Teste")


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
    return "ROBO"

def iniciarServer():
    app.run(port=5000)

if __name__ == "__main__":
    y = threading.Thread(target=iniciarServer)
    y.start()
    objeto_automacao_planilha = planilhauto()
    objeto_automacao_planilha.automacao_planilha()
    auxiliar.integrarPlanilhas()
    