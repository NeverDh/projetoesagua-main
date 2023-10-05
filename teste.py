import pandas as pd
def contarImoveis(numero):
    array = []
    contatos = pd.read_excel("contatos.xlsx")
    for index, contato in enumerate(contatos["Telefone"]):
        if str(contato) == numero:
            dados = {}
            dados["Código do imóvel"] = contatos["Código do imóvel"][index]
            dados["link"] = contatos["link"][index]
            dados["index"] = index
            array.append(dados)
    return array

imoveis = contarImoveis("968497739")

for indexImovel, imovel in enumerate (imoveis):
    mensagemImovel = f"{imovel["Código do imóvel"]} - {imovel}\n"
    print(mensagemImovel)