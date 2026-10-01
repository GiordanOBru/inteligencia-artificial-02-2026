"""Execução: python main.py [--ano 2026] [--dias 30] [--semente 42] [--sem-reparo]"""
import argparse
import random

from feriados import Calendario, UF, MUNICIPIO
from avalia_feriado import resumo_descanso
from evolucao import Parametros, executar_ag


def fmt(d):
    return f"{d:%d/%m/%Y}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ano", type=int, default=2026)
    ap.add_argument("--dias", type=int, default=30, help="30, 10, 6...")
    ap.add_argument("--semente", type=int, default=None)
    ap.add_argument("--execucoes", type=int, default=5,
                    help="reinícios independentes do AG; mostra o melhor (evita ótimo local)")
    ap.add_argument("--sem-reparo", action="store_true")
    ap.add_argument("--com-facultativos", action="store_true",
                    help="trata Carnaval e Corpus Christi como folga (ponto facultativo)")
    a = ap.parse_args()

    cal = Calendario(a.ano, incluir_facultativos=a.com_facultativos)
    params = Parametros(dias_ferias=a.dias, usar_reparo=not a.sem_reparo)
    print(f"Otimizando férias de {a.dias} dias em {a.ano} ({MUNICIPIO}-{UF})...")
    rng = random.Random(a.semente)
    res = None
    for k in range(a.execucoes):
        r = executar_ag(cal, params, rng)
        print(f"  execução {k + 1}/{a.execucoes}: melhor aptidão = {r.melhor.aptidao:.2f}")
        if res is None or r.melhor.aptidao > res.melhor.aptidao:
            res = r

    print(f"\nMelhor período de férias encontrado com fitness: {res.melhor.aptidao:.2f}\n")
    resumo = resumo_descanso(res.melhor.cromossomo, cal)
    dias_off = set()
    for n, r in enumerate(resumo, 1):
        fi, ff, qf = r["ferias"]
        di, df, qd = r["descanso"]
        print(f"Período {n}: férias {fmt(fi)} a {fmt(ff)} ({qf} dias)")
        print(f"   descanso corrido: {fmt(di)} a {fmt(df)} ({qd} dias seguidos)")
        for d, nome in r["feriados_acoplados"]:
            print(f"   + feriado colado (não gasta férias): {d:%d/%m} {nome}")
        for d, nome in r["feriados_dentro"]:
            print(f"   - feriado dentro das férias (gasta dia): {d:%d/%m} {nome}")
        for k in range(qd):
            dias_off.add(di.toordinal() + k)
    print(f"\n{a.dias} dias de férias  ->  {len(dias_off)} dias corridos de descanso "
          f"(+{len(dias_off) - a.dias} dias de folga 'de graça')")


if __name__ == "__main__":
    main()
