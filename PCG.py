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

    _validar_grafo(grafo)
    cores: Coloracao = {}

    # Processa cada vértice em ordem
    for vertice in grafo:
        # Encontra cores usadas pelos vizinhos JÁ coloridos
        cores_vizinhas = {cores[vizinho] for vizinho in grafo[vertice] if vizinho in cores}

        # Encontra a menor cor não usada pelos vizinhos
        cor = 0
        while cor in cores_vizinhas:
            cor += 1

        # Atribui essa cor ao vértice
        cores[vertice] = cor

    return cores


def Dsatur(grafo: Grafo) -> Coloracao:

    _validar_grafo(grafo)

    cores: Coloracao = {}
    saturacao: MutableMapping[str, int] = {vertice: 0 for vertice in grafo}
    graus: Dict[str, int] = {vertice: len(vizinhos) for vertice, vizinhos in grafo.items()}

    # Enquanto houver vértices não coloridos
    while len(cores) < len(grafo):
        # Encontra vértice não colorido com maior saturação (desempate por grau)
        maior_saturacao = -1
        maior_grau = -1
        escolhido = None

        for vertice in grafo:
            if vertice in cores:
                continue  # Pula vértices já coloridos

            sat = saturacao[vertice]
            grau = graus[vertice]
            # Escolhe: maior saturação, ou igual saturação + maior grau
            if sat > maior_saturacao or (sat == maior_saturacao and grau > maior_grau):
                maior_saturacao = sat
                maior_grau = grau
                escolhido = vertice

        assert escolhido is not None

        # Encontra cores usadas pelos vizinhos coloridos
        cores_vizinhas = {cores[vizinho] for vizinho in grafo[escolhido] if vizinho in cores}
        cor = 0
        while cor in cores_vizinhas:
            cor += 1

        # Atribui a menor cor disponível
        cores[escolhido] = cor

        # ATUALIZA saturação dos vizinhos não coloridos
        for vizinho in grafo[escolhido]:
            if vizinho in cores:
                continue  # Vizinho já colorido, não atualiza
            # Calcula quantas cores diferentes os vizinhos já coloridos usam
            cores_vizinhos_vizinho = {cores[outro] for outro in grafo[vizinho] if outro in cores}
            saturacao[vizinho] = len(cores_vizinhos_vizinho)

    return cores


def coloracao_backtracking(grafo: Grafo) -> Coloracao:
    _validar_grafo(grafo)

    vertices = list(grafo.keys())
    melhor_solucao: Coloracao | None = None
    melhor_numero_cores = float("inf")

    def backtrack(indice: int, cores_atual: Coloracao, cores_utilizadas: int) -> None:
        nonlocal melhor_solucao, melhor_numero_cores

        # CASO BASE: todos os vértices foram coloridos
        if indice == len(vertices):
            # Se usou menos cores que antes, atualiza melhor solução
            if cores_utilizadas < melhor_numero_cores:
                melhor_numero_cores = cores_utilizadas
                melhor_solucao = cores_atual.copy()
            return

        vertice = vertices[indice]

        # OPÇÃO 1: Tenta reutilizar cores já usadas (0 até cores_utilizadas-1)
        for cor in range(cores_utilizadas):
            # Verifica se todos vizinhos têm cor diferente (válido)
            if all(cores_atual.get(vizinho) != cor for vizinho in grafo[vertice]):
                cores_atual[vertice] = cor
                backtrack(indice + 1, cores_atual, cores_utilizadas)  # Continua recursão
                del cores_atual[vertice]  # Backtrack: desfaz atribuição

        # PODA: Se tentar uma cor nova, usaria cores_utilizadas+1
        # Se isso já é >= melhor, não vale pena explorar esse ramo
        if cores_utilizadas + 1 >= melhor_numero_cores:
            return

        # OPÇÃO 2: Tenta uma cor nova (nunca usada antes)
        cores_atual[vertice] = cores_utilizadas
        backtrack(indice + 1, cores_atual, cores_utilizadas + 1)  # Passa cores_utilizadas+1
        del cores_atual[vertice]  # Backtrack

    backtrack(0, {}, 0)

    return melhor_solucao or {}
