import requests
import time

def verificar_link():
    link_verificado = False
    while not link_verificado:
        if verificar_condicao_do_link():
            link_verificado = True
            print("Teste Sucesso CONECTADO")
        else:
            print("Teste Sucesso NÃO CONECTADO")
            time.sleep(10)

def verificar_condicao_do_link():
    try:
        response = requests.get("https://v5.chatpro.com.br/chatpro-ed90816b8e/api/v1/status")
        if response.status_code == 200:
            return True
    except Exception as e:
        pass
    return False

verificar_link()