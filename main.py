# main.py
import time
from PCV import TSPvizinhoProximo, tsp_2opt, CustoRota
from PCG import CorGulosa, Dsatur
from Tabela import tabelaPCV, tabelaPCG, Resumo

def execucaoPCV():
    print("\n=== [1] PROBLEMA DO CAIXEIRO VIAJANTE (PCV) ===")

    # Coordenadas de exemplo
    cidades = [(0, 0), (1, 3), (4, 3), (6, 1), (3, 0), (2, 2)]

    # --- Algoritmo 1: Vizinho Mais Próximo
    inicio = time.time()
    rota_gulosa = TSPvizinhoProximo(cidades)
    tempo_guloso = time.time() - inicio
    custo_guloso = CustoRota(rota_gulosa)

    # --- Algoritmo 2: 2-opt
    inicio = time.time()
    rota_2opt = tsp_2opt(rota_gulosa)
    tempo_2opt = time.time() - inicio
    custo_2opt = CustoRota(rota_2opt)

    print("\n--- Resultados PCV ---")
    print("Rota (guloso):", rota_gulosa)
    print("Rota (2-opt):", rota_2opt)

    return {
        "guloso": {"tempo": tempo_guloso, "custo": custo_guloso},
        "2opt": {"tempo": tempo_2opt, "custo": custo_2opt}
    }


def execucaoPCG():
    print("\n=== [2] PROBLEMA DA COLORAÇÃO DE GRAFOS (PCG) ===")

    grafo = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'C', 'E'],
        'C': ['A', 'B', 'D', 'E'],
        'D': ['A', 'C', 'E'],
        'E': ['B', 'C', 'D']
    }

    # --- Algoritmo 1: Guloso
    inicio = time.time()
    cores_gulosa = CorGulosa(grafo)
    TempoGulosa = time.time() - inicio
    totalCoresGulosa = max(cores_gulosa.values()) + 1

    # --- Algoritmo 2: DSATUR
    inicio = time.time()
    cores_dsat = Dsatur(grafo)
    tempoDast = time.time() - inicio
    TotoalCoresDast = max(cores_dsat.values()) + 1

    print("\n--- Resultados PCG ---")
    print("Cores (guloso):", cores_gulosa)
    print("Cores (DSATUR):", cores_dsat)

    return {
        "guloso": {"tempo": TempoGulosa, "cores": totalCoresGulosa},
        "dsat": {"tempo": tempoDast, "cores": TotoalCoresDast}
    }


if __name__ == "__main__":
    print("=== EXECUÇÃO DO PROJETO: PCV + PCG ===")
    print("Iniciando análise conjunta\n")

    resultadosPCV = execucaoPCV()
    resultadosPSG = execucaoPCG()

    tabelaPCV(resultadosPCV)
    tabelaPCG(resultadosPSG)
    Resumo(resultadosPCV, resultadosPSG)