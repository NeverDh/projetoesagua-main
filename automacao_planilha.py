from importacoes import *
import random

def enviarMensagem(mensagem, numero):
    url = "https://v5.chatpro.com.br/chatpro-b8e53cf991/api/v1/send_message"
    payload = {
    "number": numero,
    "message": mensagem
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "289dfc07e4f2d98d25fe0b778fea8035"
    }


    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

class planilhauto:

    def automacao_planilha(self):
        ##CONFIGURANDO PLANILHAS##
        ##PRIMEIRA 
        planilha = pandas.read_excel('contatos.xlsx')
        planilha_contatos = planilha['Telefone']
        planilha_codigoimoveis = planilha['Código do imóvel']
        planilha_link = planilha['link']
    
        links = []
        for link in planilha_link:
            link = str(link).split(",")
            links.append(link[1])

        ids = []
        for id in planilha_codigoimoveis:
            ids.append(id)

        ##SEGUNDA
        planilha_checados = pandas.read_excel('contatos_checados.xlsx')
        planilha_checados["Código do imóvel"] = planilha_checados["Código do imóvel"].astype(str)
        indice_planilha_contatos = planilha_checados['Telefone'].last_valid_index() +1
        indice_planilha_codigo = planilha_checados['Código do imóvel'].last_valid_index() +1
        indice_planilha_link = planilha_checados['link'].last_valid_index() +1


        #CRIANDO AS LISTAS
        numeros_exportados = []
        numero_checados = planilha_checados['Telefone'].tolist()
        codigoimoveis_exportados = []
        codigo_checados = planilha_checados['Código do imóvel'].tolist()

        for id in planilha_codigoimoveis:
            codigoimoveis_exportados.append(id)

        for numero in planilha_contatos:
            numeros_exportados.append(numero)
        dados = []
        for numeroChecados in planilha_checados['Telefone']:
            dados.append(numeroChecados)
            
        for index, numero in enumerate(planilha_contatos):
            
            if numero in numero_checados:
                print("Numero {} que solicitou agendamento no imovel {} já foi notificado".format(numero, ids[index]))
            else:
                if numero not in dados:
                    dados.append(numero)
                    mensagem = f"Olá, tudo bem? verificamos que você buscou um imóvel no nosso ZAP imóveis.\nDeseja realizar uma visita?\n1 - Sim\n2 - Não"
                    enviarMensagem(mensagem=mensagem, numero=str(numero))
                planilha_checados.loc[indice_planilha_contatos, 'Telefone'] = numero
                indice_planilha_contatos += 1
                planilha_checados.loc[indice_planilha_codigo, 'Código do imóvel'] = str(ids[index])
                indice_planilha_codigo += 1

        planilha_checados.to_excel('contatos_checados.xlsx', index=False)