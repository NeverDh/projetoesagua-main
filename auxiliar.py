import pandas as pd
from importacoes import *
import requests

def tratarDatas(datas):
    datasFormatadas = ""
    for data in datas:
        dataFormatada = f"*{data[0]}* - {data[1][8:10]}/{data[1][5:7]}/{data[1][0:4]} às {data[1][11:16]}\n"
        datasFormatadas += dataFormatada
    return datasFormatadas

def gerenciarProcesso(processo, mensagem, numero, index, datas=None, quantidade=False):
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
            inserirPlanilha(quantidade=len(datas), index=index)
            tamanhoData = len(datas)
            datas = tratarDatas(datas)
            mensagem = f"Escolha uma das datas abaixo!\nEscolha o número em negrito para selecionar a data\n\n"
            mensagem += datas
            enviarMensagem(mensagem=mensagem, numero=numero)
            atualizarPlanilha(processo=3, index=index)
            gerenciarProcesso(processo=4, numero=numero, mensagem=None, index=index, datas=datas, quantidade=tamanhoData)
        case 4:
            #MARCAR DATA NO GOOGLE AGENDA E NOTIFICAR
            print("Entrei no quatro")
            data = datas[int(mensagem)][1]
            objeto_retorna_data = RetornarData()
            datas = objeto_retorna_data.retornar_datas()
            if len(data) != quantidade:
                enviarMensagem(mensagem="Peço perdão, mas essa data não está mais disponivél!\n", numero=numero)
                gerenciarProcesso(processo=3, numero=numero, mensagem=None, index=index)
            objeto_retorna_data.retornar_datas(opcao=int(mensagem), enviar=True)
            enviarMensagem(mensagem="Data confirmada!\nAtendimento encerrado!", numero=numero)
            atualizarPlanilha(processo=5, index=index)
            inserirPlanilha(data=data, index=index)
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

def inserirPlanilha(data=None, index=None, quantidade=None, confirmado=None):
    if data:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        contatos_processo.at[index, "Data"] = data
        contatos_processo.to_excel('contatos_processo.xlsx', index=False)
    if quantidade:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        contatos_processo.at[index, "Quantidade"] = data
        contatos_processo.to_excel('contatos_processo.xlsx', index=False)
    if confirmado:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        contatos_processo.at[index, "Confirmado"] = data
        contatos_processo.to_excel('contatos_processo.xlsx', index=False)


def pegarDados(data=None, index=None, quantidade=None, confirmado=None):
    if data:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        return contatos_processo.at[index, "Data"]

    if quantidade:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        return contatos_processo.at[index, "Quantidade"]
        
    if confirmado:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        return contatos_processo.at[index, "Confirmado"]
        


def integrarPlanilhas():
    dadosArray = []
    contatos_checados = pd.read_excel("contatos_checados.xlsx")
    try:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
    except Exception as e:
        dados = {
                'Telefone': "0",
                'Processo': "0",
                'Data': "Não",
                'Confirmado': "Não",
                'Quantidade': "0"
            }

        dadosArray.append(dados)

        plan = pd.DataFrame(dadosArray)

        plan.to_excel("contatos_processo.xlsx", index=False)

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
                'Processo': 2,
                'Data': "Não",
                'Confirmado': "Não"
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
        gerenciarProcesso(processo=processoIndex[0], mensagem=mensagem, numero=numero, index=processoIndex[1]) if processoIndex != None else None
        
        

