import pandas as pd
def excluirProcessoUnico(numero):
    contatos_processo = pd.read_excel("contatos_processo.xlsx")
    dados = []
    for index, _ in enumerate(contatos_processo["Telefone"]):
        if str(numero) == str(contatos_processo["Telefone"][index]):
            dados.append(index)
    if len(dados) > 1:
        for _, indice in enumerate(index):
            if indice == 0:
                continue
            else:
                contatos_processo = contatos_processo.drop(index)
                contatos_processo.to_excel('contatos_processo.xlsx', index=False)


excluirProcessoUnico("967208668")