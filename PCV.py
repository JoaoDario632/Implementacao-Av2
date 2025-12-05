from __future__ import annotations

import itertools
import math
from typing import Iterable, List, Sequence, Tuple

Coordenada = Tuple[float, float]   # Representa uma cidade (x, y)
Rota = List[Coordenada]            # Uma rota é uma lista de cidades


def distancia(ponto_a: Coordenada, ponto_b: Coordenada) -> float:
    # Calcula a distância entre dois pontos (distância euclidiana)
    return math.dist(ponto_a, ponto_b)


def _validar_cidades(cidades: Sequence[Coordenada]) -> None:
    # Garante que a lista de cidades é válida
    if not cidades:
        raise ValueError("A lista de cidades não pode ser vazia.")
    if len(cidades) < 2:
        raise ValueError("São necessárias pelo menos duas cidades para montar uma rota.")


def TSPvizinhoProximo(cidades: Sequence[Coordenada]) -> Rota:
    # Heurística do Vizinho Mais Próximo para montar uma rota inicial
    _validar_cidades(cidades)

    inicio = cidades[0]                 # Começa pela primeira cidade
    nao_percorridos = list(cidades[1:]) # Cidades que ainda não foram visitadas
    rota = [inicio]
    atual = inicio

    # Enquanto ainda existir cidade não visitada
    while nao_percorridos:
        # Escolhe a mais próxima da cidade atual
        proxima = min(nao_percorridos, key=lambda cidade: distancia(atual, cidade))
        rota.append(proxima)
        nao_percorridos.remove(proxima) # Marca como visitada
        atual = proxima                 # Atualiza a cidade atual

    rota.append(inicio)  # Volta para o ponto inicial e fecha o ciclo
    return rota


def CustoRota(rota: Sequence[Coordenada]) -> float:
    # Soma as distâncias entre todas as cidades consecutivas da rota
    if len(rota) < 2:
        return 0.0

    return sum(distancia(rota[i], rota[i + 1]) for i in range(len(rota) - 1))


def tsp_2opt(rota_inicial: Sequence[Coordenada]) -> Rota:
    # Heurística 2-opt: tenta melhorar a rota invertendo segmentos
    if len(rota_inicial) < 4:
        return list(rota_inicial)  # Rotas muito pequenas não melhoram

    melhor = list(rota_inicial)
    custo_melhor = CustoRota(melhor)
    melhorou = True

    # Repete enquanto conseguir melhorar a rota
    while melhorou:
        melhorou = False

        # Testa todas as combinações de segmentos para inverter
        for indice_i in range(1, len(melhor) - 2):
            for indice_j in range(indice_i + 1, len(melhor) - 1):

                # Inverte o trecho da rota entre i e j
                nova_rota = (
                    melhor[:indice_i] +
                    melhor[indice_i:indice_j][::-1] +
                    melhor[indice_j:]
                )

                custo_novo = CustoRota(nova_rota)

                # Aceita a nova rota se ela for melhor
                if custo_novo < custo_melhor:
                    melhor = nova_rota
                    custo_melhor = custo_novo
                    melhorou = True

    return melhor


def tsp_bruteforce(cidades: Sequence[Coordenada]) -> Tuple[Rota, float]:
    # Resolve o PCV testando TODAS as rotas possíveis (método exato)
    # Só funciona bem com poucas cidades

    _validar_cidades(cidades)

    inicio = cidades[0]
    melhor_rota: Rota | None = None
    melhor_custo = math.inf

    # Permuta todas as possíveis ordens das cidades restantes
    for permutacao in itertools.permutations(cidades[1:]):
        # Monta a rota completa: início → permutacoes → início
        rota = [inicio, *permutacao, inicio]
        custo = CustoRota(rota)

        # Guarda a melhor rota encontrada
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_rota = rota

    return melhor_rota or [inicio], melhor_custo