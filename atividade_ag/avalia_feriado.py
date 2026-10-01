"""
FUNÇÃO DE AVALIAÇÃO
-----------------------------------------------------------------------------------
IDEIA PRINCIPAL: férias que juntam a feriados ou finais de semana, dando mais possibilidades de folga

  + dias de folga (feriado/fim de semana) COLADOS ao bloco de férias: ganho, com
    peso 3,0 (municipal/estadual), 1,5 (federal) ou 1,0 (fim de semana);
  - feriado DENTRO das férias: desperdício (mesmo peso, negativo);
  - sábado/domingo DENTRO das férias: desperdício menor (-0,5);
  + dia útil dentro das férias: 0,5 (é o uso "eficiente" do dia de férias);
  + pequeno bônus pelo tamanho do descanso corrido de cada bloco.

Penalidade: solução não factível recebe aptidão 0.0:
  - total de dias != contratado;
  - fracionamento fora da CLT (máx. 3 períodos; um >= 14 dias; demais >= 5);
  - início de período nos 2 dias que antecedem feriado/domingo (art. 134 §3º).
"""
from feriados import Calendario, Individuo, blocos_contiguos, tamanhos_validos_clt

# Pesos
PESO_FERIADO_MUN_EST = 3.0
PESO_FERIADO_FEDERAL = 1.5
PESO_FIM_DE_SEMANA = 1.0
PESO_DIA_UTIL = 0.5

PENALIDADE_FDS_DENTRO = 0.5       # sáb/dom gasto dentro das férias (metade do peso: em
BONUS_POR_DIA_DESCANSO = 0.25     # por dia do descanso corrido de cada bloco
APTIDAO_MINIMA_FACTIVEL = 0.1     # mantém soluções factíveis > 0 (roleta)


def peso_folga(calendario: Calendario, i: int) -> float:
    """Valor de um dia de folga (feriado/fim de semana); 0 para dia útil."""
    if calendario.eh_feriado_municipal(i) or calendario.eh_feriado_estadual(i):
        return PESO_FERIADO_MUN_EST
    if calendario.eh_feriado_federal(i):
        return PESO_FERIADO_FEDERAL
    if calendario.eh_fim_de_semana(i):
        return PESO_FIM_DE_SEMANA
    return 0.0


def dias_acoplados(cromossomo: list, calendario: Calendario, ini: int, tam: int):
    """Dias de folga imediatamente antes e depois do bloco (que não gastam férias)."""
    n = len(cromossomo)
    antes, k = [], ini - 1
    while k >= 0 and calendario.eh_folga(k) and cromossomo[k] == 0:
        antes.append(k)
        k -= 1
    depois, k = [], ini + tam
    while k < n and calendario.eh_folga(k) and cromossomo[k] == 0:
        depois.append(k)
        k += 1
    return antes, depois


def calcular_bonus_dias_consecutivos(cromossomo: list, calendario: Calendario) -> float:
    """Bônus pelo descanso corrido (férias + folgas coladas) de cada bloco."""
    bonus = 0.0
    for ini, tam in blocos_contiguos(cromossomo):
        antes, depois = dias_acoplados(cromossomo, calendario, ini, tam)
        bonus += BONUS_POR_DIA_DESCANSO * (tam + len(antes) + len(depois) - 1)
    return bonus


def inicios_permitidos(cromossomo: list, calendario: Calendario) -> bool:
    return all(calendario.inicio_permitido(ini) for ini, _ in blocos_contiguos(cromossomo))


def calcular_fitness(individuo: Individuo, dias_desejados: int, calendario: Calendario) -> float:
    cromossomo = individuo.cromossomo
    blocos = blocos_contiguos(cromossomo)

    # Penalidade: solução não factível -> 0.0
    if (sum(cromossomo) != dias_desejados
            or not tamanhos_validos_clt([t for _, t in blocos], dias_desejados)
            or not inicios_permitidos(cromossomo, calendario)):
        individuo.aptidao = 0.0
        return 0.0

    pontuacao = 0.0
    ganhos = set()          # união: uma folga entre dois blocos não conta em dobro
    for ini, tam in blocos:
        for dia in range(ini, ini + tam):
            if calendario.eh_feriado(dia):
                pontuacao -= peso_folga(calendario, dia)     # feriado gasto nas férias
            elif calendario.eh_fim_de_semana(dia):
                pontuacao -= PENALIDADE_FDS_DENTRO            # sáb/dom também é folga gasta
            else:
                pontuacao += PESO_DIA_UTIL
        antes, depois = dias_acoplados(cromossomo, calendario, ini, tam)
        ganhos.update(antes)
        ganhos.update(depois)

    pontuacao += sum(peso_folga(calendario, g) for g in ganhos)   # folgas "de graça"
    pontuacao += calcular_bonus_dias_consecutivos(cromossomo, calendario)

    individuo.aptidao = max(pontuacao, APTIDAO_MINIMA_FACTIVEL)
    return individuo.aptidao


def avaliar_aptidao_total(populacao: list, dias_desejados: int, calendario: Calendario) -> None:
    for ind in populacao:
        calcular_fitness(ind, dias_desejados, calendario)


def resumo_descanso(cromossomo: list, calendario: Calendario) -> list:
    """Detalha cada período: férias, descanso corrido e feriados dentro/acoplados."""
    resumo = []
    for ini, tam in blocos_contiguos(cromossomo):
        antes, depois = dias_acoplados(cromossomo, calendario, ini, tam)
        d_ini = (antes[-1] if antes else ini)
        d_fim = (depois[-1] if depois else ini + tam - 1)
        resumo.append({
            "ferias": (calendario.dias[ini], calendario.dias[ini + tam - 1], tam),
            "descanso": (calendario.dias[d_ini], calendario.dias[d_fim], d_fim - d_ini + 1),
            "feriados_dentro": [(calendario.dias[d], calendario.nome_feriado(d))
                                for d in range(ini, ini + tam) if calendario.eh_feriado(d)],
            "feriados_acoplados": [(calendario.dias[d], calendario.nome_feriado(d))
                                   for d in sorted(antes + depois) if calendario.eh_feriado(d)],
        })
    return resumo
