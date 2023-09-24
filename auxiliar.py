import pandas as pd
from datetime import datetime
import json
from importacoes import *
import requests



# objeto_retorna_data = RetornarData()
def tratarDatas(datas):
    datasFormatadas = ""
    for data in datas:
        dataFormatada = f"*{data[0]}* - {data[1][8:10]}/{data[1][5:7]}/{data[1][0:4]} às {data[1][11:28]}\n"
        datasFormatadas += dataFormatada
    return datasFormatadas

def gerenciarProcesso(processo, mensagem, numero, index):
    match processo:
        case 1:
            print("Entrei no um")
            atualizarPlanilha(processo=2, index=index)
            gerenciarProcesso(processo=2, numero=numero, mensagem=None, index=index)
        case 2:
            print("Entrei no dois")
            if str(mensagem) == "1":
                atualizarPlanilha(processo=3, index=index)
                gerenciarProcesso(processo=3, numero=numero, mensagem=None, index=index)
            else:
                atualizarPlanilha(processo=7, index=index)
        case 3:
            print("Entrei no três")
            objeto_retorna_data = RetornarData()
            datas = objeto_retorna_data.retornar_datas()
            datas = tratarDatas(datas)
            mensagem = f"Escolha uma das datas abaixo!\nEscolha o número em negrito para selecionar a data\n\n"
            mensagem += datas
            enviarMensagem(mensagem=mensagem, numero=numero)
            atualizarPlanilha(processo=4, index=index)
        case 4:
            print("Entrei no quatro")
            #MARCAR DATA NO GOOGLE AGENDA E NOTIFICAR
            objeto_retorna_data = RetornarData()
            objeto_retorna_data.retornar_datas(opcao=int(mensagem), enviar=True)
            enviarMensagem(mensagem="Data confirmada!\nAtendimento encerrado!", numero=numero)
            atualizarPlanilha(processo=5, index=index)
        case 5:
            #ENVIAR NOTIFICAÇÃO DE CONFIRMAÇÃO
            None
        case 6:
            None
        case 7:
            None

def enviarMensagem(mensagem, numero):
    url = "https://v5.chatpro.com.br/chatpro-893b2f502e/api/v1/send_message"
    payload = {
    "number": numero,
    "message": mensagem
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "3a0e2161eb1c5d3b6b525d557624ff16"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
        

def verificarProcesso(numero):
    contatos_processo = pd.read_excel("contatos_processo.xlsx")
    for index, _ in enumerate(contatos_processo["Telefone"]):
        if str(contatos_processo["Telefone"][index]) == numero:
            return contatos_processo["Processo"][index], index

def atualizarPlanilha(processo, index):
    contatos_processo = pd.read_excel("contatos_processo.xlsx")
    contatos_processo.at[index, "Processo"] = processo
    contatos_processo.to_excel('contatos_processo.xlsx', index=False)


def integrarPlanilhas():
    dadosArray = []
    contatos_checados = pd.read_excel("contatos_checados.xlsx")
    contatos_processo = pd.read_excel("contatos_processo.xlsx")

    for index, item in enumerate(contatos_processo["Telefone"]):
        dados = {
            "Telefone": contatos_processo["Telefone"][index],
            "Processo": contatos_processo["Processo"][index]
        }
        dadosArray.append(dados)

    for item in contatos_checados["Telefone"]:
        if item == 1:
            continue
        if item not in [i for i in contatos_processo["Telefone"]]:
            dados = {
                'Telefone': item,
                'Processo': 2
            }

            dadosArray.append(dados)

    plan = pd.DataFrame(dadosArray)

    plan.to_excel("contatos_processo.xlsx", index=False)



def mensagemRecebida(json):
    dados = json
    if dados["Type"] == "receveid_message":
        mensagem = dados["Body"]["Text"]
        numero = (dados["Body"]["Info"]["RemoteJid"])[4:13]
        processoIndex = verificarProcesso(numero)
        gerenciarProcesso(processo=processoIndex[0], mensagem=mensagem, numero=numero, index=processoIndex[1])
        
        

