import math


# ---------------------------------------------------------
# Função: distancia(p1, p2)
# ---------------------------------------------------------
# Calcula a distância euclidiana entre dois pontos (x1, y1) e (x2, y2)
def distancia(p1, p2):
    calculoPontos = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    return calculoPontos


# ---------------------------------------------------------
# Função: TSPvizinhoProximo(cidades)
# ---------------------------------------------------------
# Implementa a heurística do *vizinho mais próximo*:
# - Escolhe uma cidade inicial (a primeira da lista)
# - Sempre vai para a cidade mais próxima ainda não visitada
# - Retorna a rota completa, voltando à cidade inicial
#
# Parâmetros:
#   cidades: lista de tuplas (x, y) representando as coordenadas das cidades
# Retorno:
#   rota: lista de cidades na ordem visitada
# ---------------------------------------------------------
def TSPvizinhoProximo(cidades):
    inicio = cidades[0]          # Cidade inicial
    naoPercorridos = cidades[1:] # Lista das cidades restantes
    rota = [inicio]              # Rota começa pela cidade inicial
    atual = inicio               # Cidade atual

    # Enquanto ainda houver cidades a visitar
    while naoPercorridos:
        # Escolhe a cidade mais próxima da atual
        proxima = min(naoPercorridos, key=lambda c: distancia(atual, c))
        rota.append(proxima)         # Adiciona a próxima cidade à rota
        naoPercorridos.remove(proxima) # Remove do conjunto de não visitadas
        atual = proxima              # Atualiza a cidade atual

    # Retorna à cidade de origem no final (fechando o ciclo)
    rota.append(inicio)
    return rota

# Calcula o custo total (distância total percorrida) de uma rota.
# Soma a distância entre cada par consecutivo de cidades.
def CustoRota(rota):
    return sum(distancia(rota[i], rota[i + 1]) for i in range(len(rota) - 1))


# Implementa o algoritmo de otimização local *2-Opt*:
# - Tenta reduzir o custo da rota invertendo segmentos
# - Troca dois arcos (arestas) por dois novos se isso reduzir o custo
# - Continua enquanto houver melhora (método iterativo)
#
# Parâmetros:
#   rota_inicial: rota inicial (lista de cidades)
# Retorno:
#   melhor: rota otimizada após aplicar o 2-Opt
def tsp_2opt(rota_inicial):
    melhor = rota_inicial[:]             # Copia da rota original
    custoMelhor = CustoRota(melhor)      # Calcula o custo inicial
    melhorou = True                      # Flag de controle (houve melhoria?)

    # Continua enquanto houver melhoria no custo
    while melhorou:
        melhorou = False

        # Percorre todos os pares possíveis de índices (i, j)
        # e tenta inverter o trecho entre eles
        for i in range(1, len(melhor) - 2):
            for j in range(i + 1, len(melhor) - 1):

                # Cria nova rota invertendo o segmento entre i e j
                nova_rota = melhor[:i] + melhor[i:j][::-1] + melhor[j:]

                # Calcula o custo da nova rota
                custoNovo = CustoRota(nova_rota)

                # Se a nova rota for melhor (menor custo), atualiza
                if custoNovo < custoMelhor:
                    melhor = nova_rota
                    custoMelhor = custoNovo
                    melhorou = True

    # Retorna a melhor rota encontrada
    return melhor
