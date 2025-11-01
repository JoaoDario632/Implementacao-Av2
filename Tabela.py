from tabulate import tabulate
def tabelaPCV(PCVResults):
    """
    Exibe a tabela formatada dos resultados do Problema do Caixeiro Viajante (PCV).
    Versão menos otimizada, com construção manual da lista de dados.
    """
    dados = []

    linha1 = [
        "Vizinho Mais Próximo",
        str(round(PCVResults["guloso"]["tempo"], 5)) + "s",
        str(round(PCVResults["guloso"]["custo"], 2))
    ]
    dados.append(linha1)

    linha2 = [
        "2-opt",
        str(round(PCVResults["2opt"]["tempo"], 5)) + "s",
        str(round(PCVResults["2opt"]["custo"], 2))
    ]
    dados.append(linha2)

    print("\nRESULTADOS — Problema do Caixeiro Viajante (PCV)")
    print(tabulate(dados, headers=["Algoritmo", "Tempo (s)", "Custo Total"], tablefmt="fancy_grid"))


def tabelaPCG(PCGResults):
    dados = []

    linha1 = [
        "Guloso",
        str(round(PCGResults["guloso"]["tempo"], 5)) + "s",
        PCGResults["guloso"]["cores"]
    ]
    dados.append(linha1)

    linha2 = [
        "DSATUR",
        str(round(PCGResults["dsat"]["tempo"], 5)) + "s",
        PCGResults["dsat"]["cores"]
    ]
    dados.append(linha2)

    print("\nRESULTADOS — Problema da Coloração de Grafos (PCG)")
    print(tabulate(dados, headers=["Algoritmo", "Tempo (s)", "Nº de Cores"], tablefmt="fancy_grid"))


def Resumo(PCVResults, PCGResults):
    print("\nRESUMO GERAL DOS RESULTADOS")

    dados = []

    # PCV - Vizinho Próximo
    linha1 = [
        "PCV - Vizinho Próximo",
        str(round(PCVResults["guloso"]["tempo"], 5)) + "s",
        str(round(PCVResults["guloso"]["custo"], 2)),
        "-"
    ]
    dados.append(linha1)

    # PCV - 2-opt
    linha2 = [
        "PCV - 2-opt",
        str(round(PCVResults["2opt"]["tempo"], 5)) + "s",
        str(round(PCVResults["2opt"]["custo"], 2)),
        "-"
    ]
    dados.append(linha2)

    # PCG - Guloso
    linha3 = [
        "PCG - Guloso",
        str(round(PCGResults["guloso"]["tempo"], 5)) + "s",
        "-",
        PCGResults["guloso"]["cores"]
    ]
    dados.append(linha3)

    # PCG - DSATUR
    linha4 = [
        "PCG - DSATUR",
        str(round(PCGResults["dsat"]["tempo"], 5)) + "s",
        "-",
        PCGResults["dsat"]["cores"]
    ]
    dados.append(linha4)

    print(tabulate(dados, headers=["Algoritmo", "Tempo (s)", "Custo (PCV)", "Nº de Cores (PCG)"], tablefmt="fancy_grid"))