"""Funções relacionadas ao Problema do Caixeiro Viajante (PCV)."""

from __future__ import annotations

import itertools
import math
from typing import Iterable, List, Sequence, Tuple

Coordenada = Tuple[float, float]
Rota = List[Coordenada]


def distancia(ponto_a: Coordenada, ponto_b: Coordenada) -> float:
    """Calcula a distância euclidiana entre dois pontos (x1, y1) e (x2, y2)."""

    return math.dist(ponto_a, ponto_b)


def _validar_cidades(cidades: Sequence[Coordenada]) -> None:
    if not cidades:
        raise ValueError("A lista de cidades não pode ser vazia.")
    if len(cidades) < 2:
        raise ValueError("São necessárias pelo menos duas cidades para montar uma rota.")


def TSPvizinhoProximo(cidades: Sequence[Coordenada]) -> Rota:
    """Heurística do vizinho mais próximo."""

    _validar_cidades(cidades)

    inicio = cidades[0]
    nao_percorridos = list(cidades[1:])
    rota = [inicio]
    atual = inicio

    while nao_percorridos:
        proxima = min(nao_percorridos, key=lambda cidade: distancia(atual, cidade))
        rota.append(proxima)
        nao_percorridos.remove(proxima)
        atual = proxima

    rota.append(inicio)
    return rota


def CustoRota(rota: Sequence[Coordenada]) -> float:
    """Calcula o custo total (distância) de uma rota."""

    if len(rota) < 2:
        return 0.0
    return sum(distancia(rota[i], rota[i + 1]) for i in range(len(rota) - 1))


def tsp_2opt(rota_inicial: Sequence[Coordenada]) -> Rota:
    """Aplica o algoritmo 2-opt até não haver melhorias."""

    if len(rota_inicial) < 4:
        return list(rota_inicial)

    melhor = list(rota_inicial)
    custo_melhor = CustoRota(melhor)
    melhorou = True

    while melhorou:
        melhorou = False

        for indice_i in range(1, len(melhor) - 2):
            for indice_j in range(indice_i + 1, len(melhor) - 1):
                nova_rota = melhor[:indice_i] + melhor[indice_i:indice_j][::-1] + melhor[indice_j:]
                custo_novo = CustoRota(nova_rota)

                if custo_novo < custo_melhor:
                    melhor = nova_rota
                    custo_melhor = custo_novo
                    melhorou = True

    return melhor


def tsp_bruteforce(cidades: Sequence[Coordenada]) -> Tuple[Rota, float]:
    """Resolve o PCV por força bruta (apenas para instâncias pequenas)."""

    _validar_cidades(cidades)

    inicio = cidades[0]
    melhor_rota: Rota | None = None
    melhor_custo = math.inf

    for permutacao in itertools.permutations(cidades[1:]):
        rota = [inicio, *permutacao, inicio]
        custo = CustoRota(rota)
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_rota = rota

    return melhor_rota or [inicio], melhor_custo
