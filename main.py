from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from PCV import CustoRota, TSPvizinhoProximo, tsp_2opt, tsp_bruteforce
from PCG import CorGulosa, Dsatur, coloracao_backtracking
from Tabela import Resumo, tabelaPCG, tabelaPCV

Cidades = Sequence[Tuple[float, float]]
Grafo = Mapping[str, Sequence[str]]


def carregar_instancias(path: Path | None, chave: str) -> List[Dict]:
    if not path:
        return []

    with path.open("r", encoding="utf-8") as arquivo:
        conteudo = json.load(arquivo)

    instancias = conteudo.get(chave)
    if not isinstance(instancias, list):
        raise ValueError(f"Arquivo {path} não contém a chave '{chave}' com uma lista de instâncias.")
    return instancias


def normalizar_cidades(instancia: Mapping) -> Tuple[str, Cidades]:
    nome = instancia.get("nome", "instancia_sem_nome")
    cidades_brutas = instancia.get("cidades")
    if not isinstance(cidades_brutas, Iterable):
        raise ValueError(f"Instância '{nome}' não possui lista de cidades válida.")

    cidades = [tuple(map(float, cidade)) for cidade in cidades_brutas]
    return nome, cidades


def normalizar_grafo(instancia: Mapping) -> Tuple[str, Grafo]:
    nome = instancia.get("nome", "instancia_sem_nome")
    grafo = instancia.get("grafo")
    if not isinstance(grafo, Mapping):
        raise ValueError(f"Instância '{nome}' não possui um grafo válido.")
    return nome, grafo


def executar_pcv(nome: str, cidades: Cidades) -> Dict:
    # VIZINHO PRÓXIMO
    inicio = time.perf_counter()
    rota_vizinho = TSPvizinhoProximo(cidades)
    tempo_vizinho = time.perf_counter() - inicio
    custo_vizinho = CustoRota(rota_vizinho)

    # 2-OPT (melhora a solução do Vizinho Próximo)
    inicio = time.perf_counter()
    rota_2opt = tsp_2opt(rota_vizinho)
    tempo_2opt = time.perf_counter() - inicio
    custo_2opt = CustoRota(rota_2opt)

    # Variáveis para armazenar ótimo (se conseguir calcular)
    otimo = None
    fator_vizinho = None
    fator_2opt = None

    # FORÇA BRUTA (apenas para n ≤ 10)
    if len(cidades) <= 10:
        inicio = time.perf_counter()
        rota_otima, custo_otimo = tsp_bruteforce(cidades)
        tempo_otimo = time.perf_counter() - inicio
        otimo = {"rota": rota_otima, "custo": custo_otimo, "tempo": tempo_otimo}
        
        # Calcula fator de aproximação ρ
        if custo_otimo > 0:
            fator_vizinho = custo_vizinho / custo_otimo  # ρ(Vizinho Próximo)
            fator_2opt = custo_2opt / custo_otimo          # ρ(2-opt)

    return {
        "nome": nome,
        "guloso": {"tempo": tempo_vizinho, "custo": custo_vizinho, "rota": rota_vizinho, "rho": fator_vizinho},
        "2opt": {"tempo": tempo_2opt, "custo": custo_2opt, "rota": rota_2opt, "rho": fator_2opt},
        "otimo": otimo,
    }


def executar_pcg(nome: str, grafo: Grafo) -> Dict:
    # GULOSO SEQUENCIAL
    inicio = time.perf_counter()
    cores_gulosa = CorGulosa(grafo)
    tempo_guloso = time.perf_counter() - inicio
    total_cores_gulosa = max(cores_gulosa.values()) + 1 if cores_gulosa else 0

    # DSATUR (geralmente melhor que guloso)
    inicio = time.perf_counter()
    cores_dsat = Dsatur(grafo)
    tempo_dsat = time.perf_counter() - inicio
    total_cores_dsat = max(cores_dsat.values()) + 1 if cores_dsat else 0

    # Variáveis para armazenar ótimo (se conseguir calcular)
    fator_guloso = None
    fator_dsat = None
    otimo = None

    # BACKTRACKING (apenas para n ≤ 8)
    if len(grafo) <= 8:
        inicio = time.perf_counter()
        cores_otimas = coloracao_backtracking(grafo)
        tempo_otimo = time.perf_counter() - inicio
        numero_cores_otimo = max(cores_otimas.values()) + 1 if cores_otimas else 0
        otimo = {"coloracao": cores_otimas, "cores": numero_cores_otimo, "tempo": tempo_otimo}

        # Calcula fator de aproximação ρ
        if numero_cores_otimo > 0:
            fator_guloso = total_cores_gulosa / numero_cores_otimo   # ρ(Guloso)
            fator_dsat = total_cores_dsat / numero_cores_otimo       # ρ(DSATUR)

    return {
        "nome": nome,
        "guloso": {"tempo": tempo_guloso, "cores": total_cores_gulosa, "coloracao": cores_gulosa, "rho": fator_guloso},
        "dsat": {"tempo": tempo_dsat, "cores": total_cores_dsat, "coloracao": cores_dsat, "rho": fator_dsat},
        "otimo": otimo,
    }


def carregar_instancias_padrao() -> Tuple[List[Dict], List[Dict]]:
    pcv_default = [{"nome": "exemplo_base", "cidades": [(0, 0), (1, 3), (4, 3), (6, 1), (3, 0), (2, 2)]}]
    pcg_default = [{
        "nome": "exemplo_base",
        "grafo": {
            "A": ["B", "C", "D"],
            "B": ["A", "C", "E"],
            "C": ["A", "B", "D", "E"],
            "D": ["A", "C", "E"],
            "E": ["B", "C", "D"],
        },
    }]
    return pcv_default, pcg_default


def salvar_resultados(path: Path, dados: List[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Execução dos experimentos de PCV e PCG.")
    parser.add_argument("--instancias-pcv", type=Path, help="Arquivo JSON com instâncias de PCV.", default=None)
    parser.add_argument("--instancias-pcg", type=Path, help="Arquivo JSON com instâncias de PCG.", default=None)
    parser.add_argument(
        "--saida",
        type=Path,
        help="Diretório para salvar os resultados (JSON).",
        default=Path("resultados"),
    )

    argumentos = parser.parse_args()

    # Carrega instâncias dos arquivos JSON (se fornecidos)
    instancias_pcv = carregar_instancias(argumentos.instancias_pcv, "instancias_pcv")
    instancias_pcg = carregar_instancias(argumentos.instancias_pcg, "instancias_pcg")

    # Se nenhuma instância foi carregada, usa as padrões
    if not instancias_pcv and not instancias_pcg:
        instancias_pcv, instancias_pcg = carregar_instancias_padrao()

    # Executa PCV para todas as instâncias
    resultados_pcv = []
    for instancia in instancias_pcv:
        nome, cidades = normalizar_cidades(instancia)
        resultado = executar_pcv(nome, cidades)
        resultados_pcv.append(resultado)

    # Executa PCG para todas as instâncias
    resultados_pcg = []
    for instancia in instancias_pcg:
        nome, grafo = normalizar_grafo(instancia)
        resultado = executar_pcg(nome, grafo)
        resultados_pcg.append(resultado)

    # Exibe e salva resultados
    if resultados_pcv:
        tabelaPCV(resultados_pcv)  # Exibe tabela formatada
        salvar_resultados(argumentos.saida / "pcv_resultados.json", resultados_pcv)

    if resultados_pcg:
        tabelaPCG(resultados_pcg)  # Exibe tabela formatada
        salvar_resultados(argumentos.saida / "pcg_resultados.json", resultados_pcg)

    # Exibe resumo comparativo
    if resultados_pcv or resultados_pcg:
        Resumo(resultados_pcv, resultados_pcg)


if __name__ == "__main__":
    main()