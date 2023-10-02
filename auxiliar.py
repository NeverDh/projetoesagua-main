import pandas as pd
from importacoes import *
import requests

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

    # Adicionar marcador ao e-mail usando IMAP
    with imaplib.IMAP4_SSL('imap.gmail.com') as imap:
        imap.login(email, senha)
        imap.select('inbox')
        
        # Procurar pelo e-mail enviado recentemente (pode ser necessário ajustar isso)
        status, email_ids = imap.search(None, 'FROM', email)
        if status == 'OK' and email_ids:
            email_id = email_ids[0].split()[-1]  # Pega o ID do e-mail mais recente
            
            # Adicione o marcador ao e-mail (substitua 'Marcador' pelo nome do marcador desejado)
            imap.store(email_id, '+X-GM-LABELS', 'Datas')

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
            inserirPlanilha(linkImovel=True, index=index)
            gerenciarProcesso(processo=2, numero=numero, mensagem=mensagem, index=index)

        case 2:

            print("Entrei no dois")
            if str(mensagem) == "1":
                atualizarPlanilha(processo=3, index=index)
                inserirPlanilha(linkImovel=True, index=index)
                gerenciarProcesso(processo=3, numero=numero, mensagem=mensagem, index=index)
            else:
                inserirPlanilha(linkImovel=True, index=index)
                atualizarPlanilha(processo=7, index=index)

        case 3:

            print("Entrei no três")
            codImovel = pegarDados(codImovel=True, index=index)
            objeto_retorna_data = RetornarData()
            datas = objeto_retorna_data.retornar_datas(codigo_imovel=codImovel)
            tamanhoData = len(datas)
            inserirPlanilha(quantidade=tamanhoData, index=index)
            datasWP = tratarDatas(datas)
            mensagemWP = f"Escolha uma das datas abaixo!\nEscolha o número em negrito para selecionar a data\n\n"
            mensagemWP += datasWP
            enviarMensagem(mensagem=mensagemWP, numero=numero)
            atualizarPlanilha(processo=4, index=index)

        case 4:

            print("Entrei no quatro")
            codImovel = str(pegarDados(codImovel=True, index=index))
            objeto_retorna_data = RetornarData()
            datas = objeto_retorna_data.retornar_datas(codigo_imovel=codImovel)
            quantidade = int(pegarDados(index=index, quantidade=quantidade))
            if len(datas) != quantidade:
                enviarMensagem(mensagem="Peço perdão, mas houve alterações na lista de datas!\n", numero=numero)
                gerenciarProcesso(processo=3, numero=numero, mensagem=mensagem, index=index)
            dataEmail = f"{(datas[int(mensagem)][1])[8:10]}/{(datas[int(mensagem)][1])[5:7]}/{(datas[int(mensagem)][1])[0:4]} às {(datas[int(mensagem)][1])[11:16]}"
            print(dataEmail)
            data = f"{str((datas[int(mensagem)][1])[0:9])} {str((datas[int(mensagem)][1])[11:15])}"
            inserirPlanilha(data=data, index=index)
            objeto_retorna_data.retornar_datas(opcao=int(mensagem), enviar=True, codigo_imovel=codImovel)
            enviarMensagem(mensagem="Data confirmada!\nAtendimento encerrado!", numero=numero)
            linkImovel = pegarDados(linkImovel=True, index=index)
            enviarEmail(dataEmail, numero, linkImovel)
            atualizarPlanilha(processo=5, index=index)

            
        case 5:
            None
        case 6:
            None
        case 7:
            None
        case 8:
            None
            

def enviarMensagem(mensagem, numero):
    url = "https://v5.chatpro.com.br/chatpro-173eb7c207/api/v1/send_message"
    payload = {
    "number": numero,
    "message": mensagem
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "e8684a636db3f121067d9de5aa06ed80"
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

def inserirPlanilha(data=None, index=None, quantidade=None, confirmado=None, codImovel=None, linkImovel=None):

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


def pegarDados(data=None, index=None, quantidade=None, confirmado=None, codImovel=None, linkImovel=None):
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
                'linkImovel': "Não"
            }

        dadosArray.append(dados)

        plan = pd.DataFrame(dadosArray)

        plan.to_excel("contatos_processo.xlsx", index=False)

        contatos_processo = pd.read_excel("contatos_processo.xlsx")

    for index, _ in enumerate(contatos_processo["Telefone"]):
        dados = {
            "Telefone": contatos_processo["Telefone"][index],
            "Processo": contatos_processo["Processo"][index]
        }
        dadosArray.append(dados)

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
                'linkImovel': contatos_checados['linkImovel'][index]
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
        
        

