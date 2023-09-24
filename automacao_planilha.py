from importacoes import *

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

class planilhauto:
    def automacao_planilha(self):
        ##CONFIGURANDO PLANILHAS##
        ##PRIMEIRA 
        planilha = pandas.read_excel('contatos.xlsx')
        planilha_contatos = planilha['Telefone'].unique()

        ##SEGUNDA
        planilha_checados = pandas.read_excel('contatos_checados.xlsx')
        planilha_checados_contatos = planilha_checados['Telefone']
        indice_planilha_contatos = planilha_checados['Telefone'].last_valid_index() + 1

        #CRIANDO AS LISTAS
        numeros_exportados = []
        numero_checados = planilha_checados['Telefone'].tolist()

        for numero in planilha_contatos:
            numeros_exportados.append(numero)

        for numero in numeros_exportados:
            if numero in numero_checados:
                print("Numero {} já foi notificado".format(numero))
            else:
                mensagem = "Olá, tudo bem? Vimos que tem interesse em alguns de nossos imóveis.\nDeseja realizar uma visita?\n1 - Sim\n2 - Não"
                enviarMensagem(mensagem=mensagem, numero=str(numero))
                print("Mensagem enviada para o numero {}".format(numero))
                
                planilha_checados.loc[indice_planilha_contatos, 'Telefone'] = numero
                indice_planilha_contatos += 1



        planilha_checados.to_excel('contatos_checados.xlsx', index=False)