# PCV.py
import math
def distancia(p1, p2):
    calculoPontos = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    return calculoPontos

def TSPvizinhoProximo(cidades):
    inicio = cidades[0]
    naoPercorridos = cidades[1:]
    rota = [inicio]
    atual = inicio
    while naoPercorridos:
        proxima = min(naoPercorridos, key=lambda c: distancia(atual, c))
        rota.append(proxima)
        naoPercorridos.remove(proxima)
        atual = proxima
    rota.append(inicio)
    return rota

def CustoRota(rota):
    return sum(distancia(rota[i], rota[i + 1]) for i in range(len(rota) - 1))


def tsp_2opt(rota_inicial):
    melhor = rota_inicial[:]
    custoMelhor = CustoRota(melhor)
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(1, len(melhor) - 2):
            for j in range(i + 1, len(melhor) - 1):
                nova_rota = melhor[:i] + melhor[i:j][::-1] + melhor[j:]
                custoNovo = CustoRota(nova_rota)
                if custoNovo < custoMelhor:
                    melhor = nova_rota
                    custoMelhor = custoNovo
                    melhorou = True
    return melhor

