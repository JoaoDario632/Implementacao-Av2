from tabulate import tabulate


def _formatar_tempo(segundos):
    return f"{round(segundos, 5)}s" if segundos is not None else "-"


def _formatar_valor(valor, casas=2):
    return str(round(valor, casas)) if valor is not None else "-"


def _formatar_fator(rho):
    return f"{rho:.3f}" if rho is not None else "-"


def tabelaPCV(resultados):
    for instancia in resultados:
        print(f"\nRESULTADOS — PCV ({instancia['nome']})")

        dados = [
            [
                "Vizinho Mais Próximo",
                _formatar_tempo(instancia["guloso"]["tempo"]),
                _formatar_valor(instancia["guloso"]["custo"]),
                _formatar_fator(instancia["guloso"].get("rho")),
            ],
            [
                "2-opt",
                _formatar_tempo(instancia["2opt"]["tempo"]),
                _formatar_valor(instancia["2opt"]["custo"]),
                _formatar_fator(instancia["2opt"].get("rho")),
            ],
        ]

        if instancia.get("otimo"):
            dados.append([
                "Ótimo (Força Bruta)",
                _formatar_tempo(instancia["otimo"].get("tempo")),
                _formatar_valor(instancia["otimo"].get("custo")),
                "1.000",
            ])

        print(tabulate(dados, headers=["Algoritmo", "Tempo (s)", "Custo Total", "Fator ρ"], tablefmt="fancy_grid"))


def tabelaPCG(resultados):
    for instancia in resultados:
        print(f"\nRESULTADOS — PCG ({instancia['nome']})")

        dados = [
            [
                "Guloso",
                _formatar_tempo(instancia["guloso"]["tempo"]),
                instancia["guloso"]["cores"],
                _formatar_fator(instancia["guloso"].get("rho")),
            ],
            [
                "DSATUR",
                _formatar_tempo(instancia["dsat"]["tempo"]),
                instancia["dsat"]["cores"],
                _formatar_fator(instancia["dsat"].get("rho")),
            ],
        ]

        if instancia.get("otimo"):
            dados.append([
                "Ótimo (Backtracking)",
                _formatar_tempo(instancia["otimo"].get("tempo")),
                instancia["otimo"].get("cores"),
                "1.000",
            ])

        print(tabulate(dados, headers=["Algoritmo", "Tempo (s)", "Nº de Cores", "Fator ρ"], tablefmt="fancy_grid"))


def Resumo(resultados_pcv, resultados_pcg):
    print("\nRESUMO GERAL DOS RESULTADOS")

    dados = []

    for instancia in resultados_pcv:
        dados.extend([
            [
                f"PCV ({instancia['nome']}) - Vizinho Próximo",
                _formatar_tempo(instancia["guloso"]["tempo"]),
                _formatar_valor(instancia["guloso"]["custo"]),
                _formatar_fator(instancia["guloso"].get("rho")),
                "-",
            ],
            [
                f"PCV ({instancia['nome']}) - 2-opt",
                _formatar_tempo(instancia["2opt"]["tempo"]),
                _formatar_valor(instancia["2opt"]["custo"]),
                _formatar_fator(instancia["2opt"].get("rho")),
                "-",
            ],
        ])

    for instancia in resultados_pcg:
        dados.extend([
            [
                f"PCG ({instancia['nome']}) - Guloso",
                _formatar_tempo(instancia["guloso"]["tempo"]),
                "-",
                _formatar_fator(instancia["guloso"].get("rho")),
                instancia["guloso"]["cores"],
            ],
            [
                f"PCG ({instancia['nome']}) - DSATUR",
                _formatar_tempo(instancia["dsat"]["tempo"]),
                "-",
                _formatar_fator(instancia["dsat"].get("rho")),
                instancia["dsat"]["cores"],
            ],
        ])

    print(
        tabulate(
            dados,
            headers=["Algoritmo", "Tempo (s)", "Custo (PCV)", "Fator ρ", "Nº de Cores (PCG)"],
            tablefmt="fancy_grid",
        )
    )