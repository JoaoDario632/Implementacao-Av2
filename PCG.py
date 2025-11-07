"""Algoritmos de coloração de grafos (heurísticos e baseline)."""

from __future__ import annotations

from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence

Grafo = Mapping[str, Sequence[str]]
Coloracao = Dict[str, int]


def _validar_grafo(grafo: Grafo) -> None:
    if not grafo:
        raise ValueError("O grafo não pode ser vazio.")

    for vertice, vizinhos in grafo.items():
        if not isinstance(vizinhos, Iterable):
            raise TypeError(f"Os vizinhos do vértice '{vertice}' devem ser iteráveis.")
        for vizinho in vizinhos:
            if vizinho not in grafo:
                raise ValueError(f"O vértice '{vizinho}' não está declarado no grafo.")


def CorGulosa(grafo: Grafo) -> Coloracao:
    """Aplica a heurística gulosa sequencial."""

    _validar_grafo(grafo)
    cores: Coloracao = {}

    for vertice in grafo:
        cores_vizinhas = {cores[vizinho] for vizinho in grafo[vertice] if vizinho in cores}

        cor = 0
        while cor in cores_vizinhas:
            cor += 1

        cores[vertice] = cor

    return cores


def Dsatur(grafo: Grafo) -> Coloracao:
    """Aplica o algoritmo DSATUR."""

    _validar_grafo(grafo)

    cores: Coloracao = {}
    saturacao: MutableMapping[str, int] = {vertice: 0 for vertice in grafo}
    graus: Dict[str, int] = {vertice: len(vizinhos) for vertice, vizinhos in grafo.items()}

    while len(cores) < len(grafo):
        maior_saturacao = -1
        maior_grau = -1
        escolhido = None

        for vertice in grafo:
            if vertice in cores:
                continue

            sat = saturacao[vertice]
            grau = graus[vertice]
            if sat > maior_saturacao or (sat == maior_saturacao and grau > maior_grau):
                maior_saturacao = sat
                maior_grau = grau
                escolhido = vertice

        assert escolhido is not None

        cores_vizinhas = {cores[vizinho] for vizinho in grafo[escolhido] if vizinho in cores}
        cor = 0
        while cor in cores_vizinhas:
            cor += 1

        cores[escolhido] = cor

        for vizinho in grafo[escolhido]:
            if vizinho in cores:
                continue
            cores_vizinhos_vizinho = {cores[outro] for outro in grafo[vizinho] if outro in cores}
            saturacao[vizinho] = len(cores_vizinhos_vizinho)

    return cores


def coloracao_backtracking(grafo: Grafo) -> Coloracao:
    """Resolve o problema da coloração de grafos por backtracking.

    Deve ser usado apenas para instâncias pequenas como baseline.
    """

    _validar_grafo(grafo)

    vertices = list(grafo.keys())
    melhor_solucao: Coloracao | None = None
    melhor_numero_cores = float("inf")

    def backtrack(indice: int, cores_atual: Coloracao, cores_utilizadas: int) -> None:
        nonlocal melhor_solucao, melhor_numero_cores

        if indice == len(vertices):
            if cores_utilizadas < melhor_numero_cores:
                melhor_numero_cores = cores_utilizadas
                melhor_solucao = cores_atual.copy()
            return

        vertice = vertices[indice]

        for cor in range(cores_utilizadas):
            if all(cores_atual.get(vizinho) != cor for vizinho in grafo[vertice]):
                cores_atual[vertice] = cor
                backtrack(indice + 1, cores_atual, cores_utilizadas)
                del cores_atual[vertice]

        if cores_utilizadas + 1 >= melhor_numero_cores:
            return

        cores_atual[vertice] = cores_utilizadas
        backtrack(indice + 1, cores_atual, cores_utilizadas + 1)
        del cores_atual[vertice]

    backtrack(0, {}, 0)

    return melhor_solucao or {}
