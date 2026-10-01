"""
OPERADORES GENÉTICOS                         
-----------------------------------------------------------------------------------
- Seleção por roleta (proporcional à aptidão)
- Crossover de 1 ponto (taxa 65%)
- Mutação por inversão de bit (taxa 1% por gene)
"""
import random
from feriados import Individuo


def selecao_roleta(populacao: list, rng: random.Random) -> Individuo:
    soma_fitness = sum(ind.aptidao for ind in populacao)
    if soma_fitness <= 0:                        # todos inviáveis: sorteio uniforme
        return rng.choice(populacao)
    ponto_sorteado = rng.uniform(0, soma_fitness)
    acumulado = 0.0
    for ind in populacao:
        acumulado += ind.aptidao
        if acumulado >= ponto_sorteado:
            return ind
    return populacao[-1]                         # proteção contra erro de arredondamento


def crossover_um_ponto(pai1: Individuo, pai2: Individuo, taxa_crossover: float,
                       rng: random.Random):
    if rng.random() <= taxa_crossover:
        n = len(pai1.cromossomo)
        ponto = rng.randint(1, n - 1)
        filho1 = Individuo(pai1.cromossomo[:ponto] + pai2.cromossomo[ponto:])
        filho2 = Individuo(pai2.cromossomo[:ponto] + pai1.cromossomo[ponto:])
        return filho1, filho2
    return pai1.copia(), pai2.copia()


def mutacao(individuo: Individuo, taxa_mutacao: float, rng: random.Random) -> None:
    c = individuo.cromossomo
    for i in range(len(c)):
        if rng.random() <= taxa_mutacao:
            c[i] = 1 - c[i]
