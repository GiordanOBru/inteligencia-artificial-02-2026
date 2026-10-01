"""
CICLO EVOLUTIVO & SUBSTITUIÇÃO                    
-----------------------------------------------------------------------------------
- Laço principal de gerações (t = 0 até max_geracoes).
- Substituição por inclusão: une população + descendentes e mantém os N melhores.
"""
import random
from dataclasses import dataclass

from feriados import (Calendario, Individuo, gerar_populacao_inicial,
                           gerar_individuo_aleatorio, blocos_contiguos, posicionar_blocos,
                           max_periodos_permitidos, minimos_por_periodo)
from avalia_feriado import avaliar_aptidao_total
from operacao_genetica import selecao_roleta, crossover_um_ponto, mutacao


@dataclass
class Parametros:
    tamanho_populacao: int = 100
    taxa_crossover: float = 0.65
    taxa_mutacao: float = 0.01
    max_geracoes: int = 200
    dias_ferias: int = 30
    usar_reparo: bool = True


@dataclass
class Resultado:
    melhor: Individuo
    historico_melhor: list      # melhor aptidão a cada geração (t = 0..max)


def reparar(individuo: Individuo, dias_ferias: int, rng: random.Random,
            calendario: Calendario = None) -> None:
    """Transforma o filho em uma solução FACTÍVEL e válida na CLT:
    1) mantém no máx. N períodos (os maiores);
    2) ajusta os tamanhos (mín. 14 / 5 dias) e o total para `dias_ferias`;
    3) recoloca os blocos, perto das posições originais e com início permitido
       (art. 134 §3º)."""
    permitido = calendario.inicio_permitido if calendario is not None else None
    c = individuo.cromossomo
    n = len(c)

    blocos = sorted(blocos_contiguos(c), key=lambda b: -b[1])
    blocos = blocos[:max_periodos_permitidos(dias_ferias)]
    if not blocos:
        c[:] = gerar_individuo_aleatorio(n, dias_ferias, rng, calendario).cromossomo
        return

    k = len(blocos)
    inicios = [b[0] for b in blocos]
    tam = [b[1] for b in blocos]
    minimos = minimos_por_periodo(k, dias_ferias)

    tam = [max(t, m) for t, m in zip(tam, minimos)]
    while sum(tam) > dias_ferias:                       # encolhe blocos reduzíveis
        i = rng.choice([j for j in range(k) if tam[j] > minimos[j]])
        tam[i] -= 1
    while sum(tam) < dias_ferias:                       # expande blocos
        tam[rng.randrange(k)] += 1

    novo = posicionar_blocos(tam, n, rng, preferidos=inicios, permitido=permitido)
    if novo is None:                                    # não coube: recomeça
        novo = gerar_individuo_aleatorio(n, dias_ferias, rng, calendario).cromossomo
    c[:] = novo


def selecionar_melhores(conjunto: list, n: int) -> list:
    return sorted(conjunto, key=lambda ind: ind.aptidao, reverse=True)[:n]


def executar_ag(calendario: Calendario, params: Parametros,
                rng: random.Random = None, verbose: bool = False) -> Resultado:
    rng = rng or random.Random()
    n_dias = calendario.total_dias

    geracao = 0
    populacao = gerar_populacao_inicial(params.tamanho_populacao, n_dias,
                                        params.dias_ferias, rng, calendario)
    avaliar_aptidao_total(populacao, params.dias_ferias, calendario)
    historico = [max(i.aptidao for i in populacao)]

    while geracao < params.max_geracoes:
        descendentes = []
        while len(descendentes) < params.tamanho_populacao:
            pai1 = selecao_roleta(populacao, rng)
            pai2 = selecao_roleta(populacao, rng)
            filho1, filho2 = crossover_um_ponto(pai1, pai2, params.taxa_crossover, rng)
            mutacao(filho1, params.taxa_mutacao, rng)
            mutacao(filho2, params.taxa_mutacao, rng)
            if params.usar_reparo:
                reparar(filho1, params.dias_ferias, rng, calendario)
                reparar(filho2, params.dias_ferias, rng, calendario)
            descendentes.extend([filho1, filho2])

        avaliar_aptidao_total(descendentes, params.dias_ferias, calendario)

        # Substituição por inclusão: união e seleção dos N melhores
        populacao = selecionar_melhores(populacao + descendentes, params.tamanho_populacao)
        geracao += 1
        historico.append(populacao[0].aptidao)
        if verbose and geracao % 20 == 0:
            print(f"  geração {geracao:>3}: melhor aptidão = {populacao[0].aptidao:.2f}")

    return Resultado(melhor=populacao[0], historico_melhor=historico)
