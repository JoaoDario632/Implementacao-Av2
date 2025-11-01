# PCG.py
import time
def CorGulosa(grafo):
    cores = {}

    for vertice in grafo:
        coresVizinhas = []
        for vizinho in grafo[vertice]:
            if vizinho in cores:
                coresVizinhas.append(cores[vizinho])

        cor = 0
        while cor in coresVizinhas:
            cor += 1

        cores[vertice] = cor

    return cores
def Dsatur(grafo):
    cores = {}
    saturacao = {}
    graus = {}

    for vertice in grafo:
        saturacao[vertice] = 0
        graus[vertice] = len(grafo[vertice])

    while len(cores) < len(grafo):
        maiorSat = -1
        maiorGrau = -1
        escolhido = None

        for v in grafo:
            if v not in cores:
                sat = saturacao[v]
                grau = graus[v]
                if sat > maiorSat or (sat == maiorSat and grau > maiorGrau):
                    maiorSat = sat
                    maiorGrau = grau
                    escolhido = v

        coresVizinhas = []
        for u in grafo[escolhido]:
            if u in cores:
                coresVizinhas.append(cores[u])

        cor = 0
        while cor in coresVizinhas:
            cor += 1

        cores[escolhido] = cor

        # Atualizar saturação dos vizinhos não coloridos
        for u in grafo[escolhido]:
            if u not in cores:
                coresVizinhosU = []
                for w in grafo[u]:
                    if w in cores:
                        coresVizinhosU.append(cores[w])
                saturacao[u] = len(set(coresVizinhosU))

    return cores