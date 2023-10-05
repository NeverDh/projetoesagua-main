import pandas as pd
def pegarIndex(numero, indexImovel):
    imoveis = []
    contatos_processo = pd.read_excel("contatos_processo.xlsx")
    for index, _ in enumerate(contatos_processo["Telefone"]):
        dados = {}
        if str(contatos_processo["Telefone"][index]) == str(numero):
            dados["index"] = index
            # dados["imovel"] = contato["Código do imóvel"]
            dados["imovel"] = contatos_processo["codImovel"][index]
            imoveis.append(dados)
    for _ in imoveis[int(indexImovel)]:
        for indexThird, _ in enumerate(contatos_processo["Telefone"]):

            if str(imoveis[int(indexImovel)]["imovel"]) == str(contatos_processo["codImovel"][indexThird]) and str(numero == str(contatos_processo["Telefone"][indexThird])):
                return indexThird
            
