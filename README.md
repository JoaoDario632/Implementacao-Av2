# 🧩 Projeto de Algoritmos: PCV + PCG

Este projeto implementa dois **algoritmos clássicos de Inteligência Computacional**:

1. **PCV (Problema do Caixeiro Viajante)** – otimização de rotas.  
2. **PCG (Problema da Coloração de Grafos)** – coloração eficiente de vértices de um grafo.  

O objetivo é **comparar heurísticas e algoritmos exatos** para ambos os problemas e apresentar os resultados de forma tabular.

---

## 📂 Estrutura do Projeto
├── main.py # Programa principal, executa PCV + PCG
├── PCV.py # Funções do Problema do Caixeiro Viajante
├── PCG.py # Funções do Problema da Coloração de Grafos
├── Tabela.py # Funções para exibir os resultados em tabelas
├── README.md # Documentação do projeto

---

## 🔹 Funcionalidades

### 1️⃣ PCV – Problema do Caixeiro Viajante

- Recebe uma lista de coordenadas de cidades.  
- **Algoritmos implementados:**
  - **Vizinho Mais Próximo (Guloso)**: forma uma rota inicial aproximada.  
  - **2-opt**: otimiza a rota obtida pelo vizinho mais próximo.  
- Calcula:
  - **Custo total da rota** (distância percorrida).  
  - **Tempo de execução** de cada algoritmo.  

### 2️⃣ PCG – Problema da Coloração de Grafos

- Recebe um grafo definido como dicionário `{vértice: [vizinhos]}`.  
- **Algoritmos implementados:**
  - **Guloso**: colore vértices sequencialmente, evitando cores já usadas nos vizinhos.  
  - **DSATUR**: escolhe o próximo vértice com maior saturação (mais restrito), resultando em menos cores.  
- Calcula:
  - **Número de cores utilizadas** para colorir o grafo.  
  - **Tempo de execução** de cada algoritmo.  
---

## 📊 Saída do Programa

- Exibe os resultados em **tabelas formatadas** usando a biblioteca `tabulate`.
- **Resumo geral** com:
  - PCV: tempo e custo total.  
  - PCG: tempo e número de cores.

Exemplo de tabela gerada:

| Algoritmo            | Tempo (s) | Custo Total |
|---------------------|-----------|-------------|
| Vizinho Mais Próximo | 0.00123   | 15.42       |
| 2-opt                | 0.00234   | 12.98       |

| Algoritmo | Tempo (s) | Nº de Cores |
|-----------|-----------|------------|
| Guloso    | 0.00056   | 3          |
| DSATUR    | 0.00078   | 2          |

---

## ⚙️ Como Executar

1. Certifique-se de ter **Python 3** instalado.  
2. Instale a dependência para tabelas:

```bash
pip install tabulate

## Dependências Usadas

Este projeto uso da biblioteca tabulete, a qual realiza a formatação de dados tabulares, para que eles possa ser exibidos de forma legível
> Para instalar a depedencia, rode o comando:
  pip install tabulate
# 👨‍💻 Autores
<table>
  <tr>
     <td align="center">
            <a href="https://github.com/JoaoDario632">
         <img src="https://avatars.githubusercontent.com/u/134674876?v=4" style="border-radius: 50%" width="100px;" alt="ferreira"/>
         <br />
         <sub><b>João Dário 💻👑</b></sub>
       </a>
     </td>
    <td align="center">
       <a href="https://github.com/LucasAugustoSS">
         <img src="https://avatars.githubusercontent.com/u/126918429?v=4" style="border-radius: 50%" width="100px;" alt="Lucas augusto"/>
         <br />
         <sub><b>Lucas Augusto 💻👑</b></sub>
       </a>
     </td>
     <td align="center">
          <a href="https://github.com/FrrTiago">
         <img src="https://avatars.githubusercontent.com/u/132114628?v=4" style="border-radius: 50%" width="100px;" alt="ferreira"/>
         <br />
         <sub><b>Tiago Ferreira 💻</b></sub>
       </a>
     </td>
  </tr>
</table>