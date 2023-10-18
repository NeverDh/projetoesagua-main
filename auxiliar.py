import pandas as pd
from importacoes import *
import requests

def encaminharMensagem(mensagem, numero):
    mensagemWP = f"O contato {numero}, contatou o suporte com a seguinte mensagem:\n"
    mensagemWP += mensagem
    enviarMensagem(mensagem=mensagemWP, numero="21990033942")

def verificarProcesso(numero):
    contatos_processo = pd.read_excel("contatos_processo.xlsx")
    for index, _ in enumerate(contatos_processo["Telefone"]):
        if str(contatos_processo["Telefone"][index]) == str(numero):
            return contatos_processo["Processo"][index], index

def excluirProcessoUnico(numero):
    contatos_processo = pd.read_excel("contatos_processo.xlsx")
    dados = []
    i = 0
    for index, _ in enumerate(contatos_processo["Telefone"]):
        if str(numero) == str(contatos_processo["Telefone"][index]):
            dados.append(index)
            i = index
    if len(dados) > 1:
        for indice in range(i):
            if indice == 0:
                continue
            else:
                contatos_processo = contatos_processo.drop(indice )
                contatos_processo.to_excel('contatos_processo.xlsx', index=False)
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        for index, _ in enumerate(contatos_processo["Telefone"]):
            if str(numero) == str(contatos_processo["Telefone"][index]):
                return index
    return False

    

def excluirProcesso(imovel, numero):
    contatos_processo = pd.read_excel("contatos_processo.xlsx")
    for index, _ in enumerate(contatos_processo["Telefone"]):
        if str(numero) == str(contatos_processo["Telefone"][index]) and str(imovel) != str(contatos_processo["codImovel"][index]):
            contatos_processo = contatos_processo.drop(index)
            contatos_processo.to_excel('contatos_processo.xlsx', index=False)

def contarImoveis(numero):
    array = []
    contatos = pd.read_excel("contatos.xlsx")
    for index, contato in enumerate(contatos["Telefone"]):
        if str(contato) == numero:
            dados = {}
            dados["Código do imóvel"] = contatos["Código do imóvel"][index]
            link = str(contatos["link"][index]).split(",")
            dados["link"] = link[1]
            dados["index"] = index
            array.append(dados)
    return array

def pegarIndex(numero, indexImovel):
    imoveis = []
    contatos_processo = pd.read_excel("contatos_processo.xlsx")
    for index, _ in enumerate(contatos_processo["Telefone"]):
        dados = {}
        if str(contatos_processo["Telefone"][index]) == str(numero):
            dados["index"] = index
            dados["imovel"] = contatos_processo["codImovel"][index]
            imoveis.append(dados)
    for _ in imoveis[int(indexImovel)]:
        for indexThird, _ in enumerate(contatos_processo["Telefone"]):
            if str(imoveis[int(indexImovel)]["imovel"]) == str(contatos_processo["codImovel"][indexThird]) and str(numero == str(contatos_processo["Telefone"][indexThird])):
                return indexThird

def enviarEmail(data, numero, linkImovel):
    email = 'itaimoveis7@gmail.com'
    senha = 'qrcswpxbuienlyze'

    msg= EmailMessage()
    msg['Subject'] = 'Agendamento feito'
    msg['From'] = 'itaimoveis7@gmail.com'
    msg['To'] = 'itaimoveis7@gmail.com'
    mensagem_html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                width: 100%;
                height: 100%;
            }}
            .container {{
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                width: 60%;
                height: 60%;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Agendamento feito</h1>
            <p>Olá, Gostaria de compartilhar uma ótima notícia! Um novo horário foi agendado com sucesso através do nosso robô de WhatsApp. Abaixo estão os detalhes do agendamento:</p>
            <ul>
                <li>Data e Horário: {data}</li>
                <li>Contato do Cliente: {numero}</li>
                <li>Link do imóvel: {linkImovel}</li>
            </ul>
            <p>Atenciosamente,<br>Robô Ita Imóveis</p>
        </div>
    </body>
    </html>
    """

    msg.add_alternative(mensagem_html, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, senha)
        smtp.send_message(msg)

def tratarData(data):
    dataFormatada = f"{data[8:10]}/{data[5:7]}/{data[0:4]} às {data[11:16]}\n"
    return dataFormatada

def tratarDatas(datas):
    datasFormatadas = ""
    for data in datas:
        dataFormatada = f"*{data[0]}* - {data[1][8:10]}/{data[1][5:7]}/{data[1][0:4]} às {data[1][11:16]}\n"
        datasFormatadas += dataFormatada
    return datasFormatadas

def gerenciarProcesso(processo, mensagem, numero, index, datas=None, quantidade=False, multiplos=True, reagendamento=False):
    match processo:
        case 1:

            print("Entrei no um")
            atualizarPlanilha(processo=2, index=index)
            gerenciarProcesso(processo=2, numero=numero, mensagem=mensagem, index=index)

        case 2:
            print("Entrei no dois")
            if reagendamento == True:
                mensagem = "1" 
            if str(mensagem) == "1":
                imoveis = contarImoveis(numero)
                if len(imoveis) == 1:
                    gerenciarProcesso(processo=3, numero=numero, index=index, mensagem=mensagem, multiplos=False)
                else:
                    enviarMensagem(mensagem="Pra qual imóvel você deseja agendar?\nAguarde trazendo os imóveis...\n", numero=numero)
                    for indexImov, imovel in enumerate(imoveis):
                        mensagemImovel = f"{imovel['link']}\n\n{indexImov} - {imovel['Código do imóvel']}\n"
                        if indexImov + 1 < len(imoveis):
                            mensagemImovel += f"Aguarde trazendo os imóveis...\n"
                        else:
                            mensagemImovel += f"Todos os imóveis disponíveis acima!\n"
                        enviarMensagem(mensagem=mensagemImovel, numero=numero)
                        atualizarPlanilha(processo=3, index=index)
            elif str(mensagem) == "2":
                indexUnico = excluirProcessoUnico(numero)
                atualizarPlanilha(processo=7, index=index if indexUnico == False else indexUnico)
                gerenciarProcesso(processo=7, numero=numero, index=index if indexUnico == False else indexUnico, mensagem=mensagem)
            else:
                enviarMensagem(mensagem="Opção inválida! Por favor escolha uma das opções acima.\n", numero=numero)

        case 3:

            print("Entrei no três")
            if multiplos == True:
                try:
                    indexImovel = pegarIndex(numero, mensagem)
                except Exception as e:
                    print(e)
                    print("ERRO CONTROLADO")
                    enviarMensagem(mensagem="Opção inválida! Por favor escolha uma das opções acima.\n", numero=numero)
                    return None
            codImovel = pegarDados(codImovel=True, index=indexImovel if multiplos == True else index)
            try:
                objeto_retorna_data = RetornarData()
                datas = objeto_retorna_data.retornar_datas(codigo_imovel=codImovel)
                tamanhoData = len(datas)
            except Exception as e:
                print(e)
                print("ERRO CONTROLADO")
                enviarMensagem(mensagem=f"Sem datas disponiveis pro imóvel {codImovel}\nPor favor, tente outro dia!", numero=numero)
                return None
            datasWP = tratarDatas(datas)
            mensagemWP = f"Escolha uma das datas abaixo!\nEscolha o número em negrito para selecionar a data\n\n"
            mensagemWP += datasWP
            enviarMensagem(mensagem=mensagemWP, numero=numero)
            excluirProcesso(codImovel, numero)
            inserirPlanilha(quantidade=tamanhoData, index=index)
            atualizarPlanilha(processo=4, index=index)

        case 4:

            print("Entrei no quatro")
            codImovel = str(pegarDados(codImovel=True, index=index))
            try:
                objeto_retorna_data = RetornarData()
                datas = objeto_retorna_data.retornar_datas(codigo_imovel=codImovel)
                quantidade = int(pegarDados(index=index, quantidade=quantidade))
                if len(datas) != quantidade:
                    enviarMensagem(mensagem="Peço perdão, mas houve alterações na lista de datas!\n", numero=numero)
                    gerenciarProcesso(processo=3, numero=numero, mensagem=mensagem, index=index)
            except Exception as e:
                print(e)
                print("ERRO CONTROLADO")
                enviarMensagem(mensagem="Peço perdão, mas houve alterações na lista de datas!\n", numero=numero)
                enviarMensagem(mensagem=f"Sem datas disponiveis pro imóvel {codImovel}\nPor favor, tente outro dia!", numero=numero)
                return None
            try:
                dataEmail = f"{(datas[int(mensagem)][1])[8:10]}/{(datas[int(mensagem)][1])[5:7]}/{(datas[int(mensagem)][1])[0:4]} às {(datas[int(mensagem)][1])[11:16]}"
                data = f"{str((datas[int(mensagem)][1])[0:9])} {str((datas[int(mensagem)][1])[11:16])}"
                inserirPlanilha(data=data, index=index)
            except Exception as e:
                print(e)
                print("ERRO CONTROLADO")
                enviarMensagem(mensagem=f'Opção inválida! Por favor, escolha uma das opções acima.', numero=numero)
                return None
            try:
                objeto_retorna_data.retornar_datas(opcao=int(mensagem), enviar=True, codigo_imovel=codImovel, numero=numero)
            except Exception as e:
                print(e)
                print("ERRO CONTROLADO")
                enviarMensagem(mensagem="Opção inválida! Por favor escolha uma das datas acima.\n", numero=numero)
                return None
            enviarMensagem(mensagem="Data confirmada!\nAtendimento encerrado!", numero=numero)
            linkImovel = pegarDados(linkImovel=True, index=index)
            enviarEmail(dataEmail, numero, linkImovel)
            atualizarPlanilha(processo=5, index=index)

        case 5:

            codImovel = pegarDados(codImovel=True, index=index)
            if str(mensagem) == "1":
                inserirPlanilha(confirmado=True, index=index)
                enviarMensagem(mensagem=f'O contato {numero} confirmou a presença no imóvel: {codImovel}', numero="21992193853")
            elif str(mensagem) == "2":
                inserirPlanilha(confirmado=False, index=index)
                enviarMensagem(mensagem=f'Deseja remarcar a visitação?\n1 - Sim\n2 - Não', numero=numero)
                atualizarPlanilha(processo=6, index=index)
            else:
                enviarMensagem(mensagem=f'Opção inválida! Por favor, escolha uma das opções acima.', numero=numero)
           
        case 6:

   
            codImovel = pegarDados(codImovel=True, index=index)
            if str(mensagem) == "1":
                objeto_excluir_data = excluiragendamento()
                objeto_excluir_data.removeragendamento(numero=numero, codigo_imovel=codImovel)
                inserirPlanilha(confirmado=True, index=index)
                enviarMensagem(mensagem=f'O contato {numero} reagendou a presença no imóvel: {codImovel}', numero="21992193853")
                atualizarPlanilha(processo=2, index=index)
                gerenciarProcesso(processo=2, numero=numero, mensagem=mensagem, index=index, reagendamento=True)
            elif str(mensagem) == "2":
                objeto_excluir_data = excluiragendamento()
                objeto_excluir_data.removeragendamento(numero=numero, codigo_imovel=codImovel)
                inserirPlanilha(confirmado=False, index=index)
                enviarMensagem(mensagem=f'O contato {numero} cancelou a presença no imóvel: {codImovel}', numero="21992193853")
                atualizarPlanilha(processo=9, index=index)
            else:
                enviarMensagem(mensagem=f'Opção inválida! Por favor, escolha uma das opções acima.', numero=numero)

                
        case 7:

            enviarMensagem(mensagem="Deseja deixar uma mensagem para o suporte?\n1 - Sim\n2 - Não", numero=numero)
            atualizarPlanilha(processo=8, index=index)

            
        case 8:
                
            if str(mensagem) == "1":
                inserirPlanilha(suporte=True, index=index)
                atualizarPlanilha(processo=9, index=index)
            elif str(mensagem) == "2":
                enviarMensagem(mensagem="Obrigado pelo contato! ;)", numero=numero)
                atualizarPlanilha(processo=9, index=index)
            else:
                enviarMensagem(mensagem=f'Opção inválida! Por favor, escolha uma das opções acima.', numero=numero)

        case 9:
            
            x = pegarDados(suporte=True, index=index)
            if x == True:
                encaminharMensagem(mensagem, numero)



def enviarMensagem(mensagem, numero):
    url = "https://v5.chatpro.com.br/chatpro-459d5f834c/api/v1/send_message"
    payload = {
    "number": numero,
    "message": mensagem
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "c90e811e39d80f5666a236ce114b75f1"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def atualizarPlanilha(processo, index):
    contatos_processo = pd.read_excel("contatos_processo.xlsx")
    contatos_processo.at[index, "Processo"] = processo
    contatos_processo.to_excel('contatos_processo.xlsx', index=False)

def inserirPlanilha(data=None, index=None, quantidade=None, confirmado=None, codImovel=None, linkImovel=None, suporte=None):

    print("INSERIR PLANILHA")
    if data != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        contatos_processo.at[index, "Data"] = data
        contatos_processo.to_excel('contatos_processo.xlsx', index=False)

    if quantidade != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        contatos_processo.at[index, "Quantidade"] = quantidade
        contatos_processo.to_excel('contatos_processo.xlsx', index=False)

    if confirmado != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        contatos_processo.at[index, "Confirmado"] = confirmado
        contatos_processo.to_excel('contatos_processo.xlsx', index=False)

    if codImovel != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        contatos_processo.at[index, "codImovel"] = codImovel
        contatos_processo.to_excel('contatos_processo.xlsx', index=False)

    if linkImovel != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        contatos_processo.at[index, "linkImovel"] = linkImovel
        contatos_processo.to_excel('contatos_processo.xlsx', index=False)
    if suporte != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        contatos_processo.at[index, "suporte"] = suporte
        contatos_processo.to_excel('contatos_processo.xlsx', index=False)


def pegarDados(data=None, index=None, quantidade=None, confirmado=None, codImovel=None, linkImovel=None, suporte=None):
    if data != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        return contatos_processo.at[index, "Data"]

    if quantidade != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        return contatos_processo.at[index, "Quantidade"]
        
    if confirmado != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        return contatos_processo.at[index, "Confirmado"]
    
    if codImovel != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        return contatos_processo.at[index, "codImovel"]
    
    if linkImovel != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        return contatos_processo.at[index, "linkImovel"]
    
    if suporte != None:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        return contatos_processo.at[index, "suporte"]
        


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
                'Quantidade': "0",
                'codImovel': "Não",
                'linkImovel': "Não",
                'suporte': "Não"
            }

        dadosArray.append(dados)

        plan = pd.DataFrame(dadosArray)

        plan.to_excel("contatos_processo.xlsx", index=False)

        contatos_processo = pd.read_excel("contatos_processo.xlsx")

    for index, item in enumerate(contatos_checados["Telefone"]):
        if item == 1:
            continue
        if item not in [i for i in contatos_processo["Telefone"]]:
            dados = {
                'Telefone': item,
                'Processo': 2,
                'Data': "Não",
                'Confirmado': "Não",
                'Quantidade': "0",
                'codImovel': contatos_checados['Código do imóvel'][index],
                'linkImovel': contatos_checados['link'][index],
                'suporte': "Não"
            }

            dadosArray.append(dados)

    if len(dadosArray) > 0:
        plan = pd.DataFrame(dadosArray)

        plan.to_excel("contatos_processo.xlsx", index=False)



def mensagemRecebida(json):
    dados = json
    if dados["Type"] == "receveid_message":
        mensagem = dados["Body"]["Text"]
        numero = (dados["Body"]["Info"]["RemoteJid"])[2:13]
        processoIndex = verificarProcesso(numero)
        gerenciarProcesso(processo=processoIndex[0], mensagem=mensagem, numero=numero, index=processoIndex[1]) if processoIndex != None else None
        
        

