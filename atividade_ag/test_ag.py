"""Testes: python -m unittest -v"""
import random
import unittest
from datetime import date

from feriados import (Calendario, Individuo, calcular_pascoa, gerar_individuo_aleatorio,
                           blocos_contiguos, tamanhos_validos_clt)
from avalia_feriado import calcular_fitness, resumo_descanso
from operacao_genetica import selecao_roleta, crossover_um_ponto, mutacao
from evolucao import Parametros, executar_ag, reparar


def idx(m, d, ano=2026):
    return date(ano, m, d).timetuple().tm_yday - 1


def tams(ind):
    return [t for _, t in blocos_contiguos(ind.cromossomo)]


def cromo(blocos, n=365):
    """blocos = [(indice_inicial, tamanho), ...]"""
    c = [0] * n
    for ini, t in blocos:
        for d in range(ini, ini + t):
            c[d] = 1
    return Individuo(c)


class TestAG(unittest.TestCase):
    def setUp(self):
        self.cal = Calendario(2026)
        self.rng = random.Random(1)

    def test_calendario(self):
        self.assertEqual(self.cal.total_dias, 365)
        self.assertEqual(calcular_pascoa(2026), date(2026, 4, 5))
        self.assertTrue(self.cal.eh_feriado_estadual(idx(10, 5)))
        self.assertTrue(self.cal.eh_feriado_municipal(idx(5, 20)))

    def test_ponto_facultativo_nao_e_feriado_por_padrao(self):
        self.assertFalse(self.cal.eh_feriado(idx(2, 16)))            # Carnaval 2026
        cal2 = Calendario(2026, incluir_facultativos=True)
        self.assertTrue(cal2.eh_feriado(idx(2, 16)))

    def test_nao_gastar_sabado_nas_ferias(self):
        # 12 dias: terminar na sexta (sábado/domingo colados) vale mais que terminar no sábado
        sexta = cromo([(idx(3, 2), 12)])       # seg 2/3 a sex 13/3
        sabado = cromo([(idx(3, 3), 12)])      # ter 3/3 a sáb 14/3
        self.assertGreater(calcular_fitness(sexta, 12, self.cal), calcular_fitness(sabado, 12, self.cal))

    # ---- CLT: fracionamento ----
    def test_regra_clt_tamanhos(self):
        self.assertTrue(tamanhos_validos_clt([30], 30))
        self.assertTrue(tamanhos_validos_clt([14, 16], 30))
        self.assertTrue(tamanhos_validos_clt([20, 5, 5], 30))
        self.assertFalse(tamanhos_validos_clt([25, 4, 1], 30))
        self.assertFalse(tamanhos_validos_clt([13, 12, 5], 30))
        self.assertFalse(tamanhos_validos_clt([10, 10, 5, 5], 30))
        self.assertFalse(tamanhos_validos_clt([10, 10, 10], 30))
        self.assertTrue(tamanhos_validos_clt([10], 10))
        self.assertFalse(tamanhos_validos_clt([5, 5], 10))

    def test_fitness_respeita_fracionamento(self):
        seg = [idx(1, 5), idx(3, 2), idx(6, 8)]            # três segundas-feiras
        self.assertGreater(calcular_fitness(cromo([(seg[0], 20), (seg[1], 5), (seg[2], 5)]), 30, self.cal), 0)
        self.assertEqual(calcular_fitness(cromo([(seg[0], 26), (seg[1], 4)]), 30, self.cal), 0.0)
        quatro = cromo([(seg[0], 10), (idx(2, 2), 10), (seg[1], 5), (seg[2], 5)])
        self.assertEqual(calcular_fitness(quatro, 30, self.cal), 0.0)

    def test_fitness_inviavel_zero(self):
        ind = gerar_individuo_aleatorio(365, 29, self.rng, self.cal)
        self.assertEqual(calcular_fitness(ind, 30, self.cal), 0.0)

    # ---- CLT: início das férias (art. 134 §3º) ----
    def test_inicio_permitido(self):
        self.assertFalse(self.cal.inicio_permitido(idx(1, 9)))    # sexta (domingo em 2 dias)
        self.assertFalse(self.cal.inicio_permitido(idx(1, 10)))   # sábado
        self.assertFalse(self.cal.inicio_permitido(idx(10, 3)))   # sábado antes de feriado seg 5/10
        self.assertFalse(self.cal.inicio_permitido(idx(12, 23)))  # 2 dias antes do Natal
        self.assertTrue(self.cal.inicio_permitido(idx(1, 5)))     # segunda comum

    def test_fitness_zero_se_inicio_proibido(self):
        self.assertEqual(calcular_fitness(cromo([(idx(1, 9), 30)]), 30, self.cal), 0.0)
        self.assertGreater(calcular_fitness(cromo([(idx(1, 5), 30)]), 30, self.cal), 0.0)

    # ---- ideia principal: feriado colado x feriado gasto ----
    def test_feriado_colado_vale_mais(self):
        # 5/10/2026 (seg) é feriado estadual. Começar na terça 6/10 "cola" feriado+fim de semana.
        colado = cromo([(idx(10, 6), 14)])
        longe = cromo([(idx(10, 7), 14)])
        self.assertGreater(calcular_fitness(colado, 14, self.cal), calcular_fitness(longe, 14, self.cal))
        r = resumo_descanso(colado.cromossomo, self.cal)[0]
        self.assertEqual(r["descanso"][0], date(2026, 10, 3))     # descanso começa no sábado
        self.assertEqual(r["descanso"][2], 17)                    # 14 férias + sáb + dom + feriado
        self.assertEqual(len(r["feriados_acoplados"]), 1)

    def test_feriado_dentro_penaliza(self):
        # mesmo tamanho de bloco; um contém o feriado de 12/10, o outro não
        com = cromo([(idx(10, 6), 14)])      # 6 a 19/10 -> contém 12/10 (federal)
        sem = cromo([(idx(10, 13), 14)])     # 13 a 26/10 -> sem feriado
        r_com = resumo_descanso(com.cromossomo, self.cal)[0]
        self.assertEqual(len(r_com["feriados_dentro"]), 1)
        self.assertEqual(len(resumo_descanso(sem.cromossomo, self.cal)[0]["feriados_dentro"]), 0)

    # ---- população, operadores, reparo, AG ----
    def test_populacao_inicial_valida(self):
        for dias in (30, 10, 6):
            for _ in range(200):
                ind = gerar_individuo_aleatorio(365, dias, self.rng, self.cal)
                self.assertTrue(tamanhos_validos_clt(tams(ind), dias))
                self.assertGreater(calcular_fitness(ind, dias, self.cal), 0)

    def test_operadores(self):
        pop = [gerar_individuo_aleatorio(365, 30, self.rng, self.cal) for _ in range(10)]
        for p in pop:
            calcular_fitness(p, 30, self.cal)
        self.assertIn(selecao_roleta(pop, self.rng), pop)
        f1, f2 = crossover_um_ponto(pop[0], pop[1], 1.0, self.rng)
        self.assertEqual(len(f1.cromossomo), 365)
        antes = pop[0].cromossomo[:]
        mutacao(pop[0], 0.0, self.rng)
        self.assertEqual(antes, pop[0].cromossomo)

    def test_reparo_gera_solucao_factivel(self):
        casos = [Individuo([1] * 50 + [0] * 315),
                 Individuo([0] * 365),
                 Individuo([1, 0] * 100 + [0] * 165),
                 cromo([(10, 3), (50, 3), (90, 3), (130, 3), (170, 3)])]
        for _ in range(300):
            casos.append(Individuo([self.rng.randint(0, 1) for _ in range(365)]))
        for ind in casos:
            reparar(ind, 30, self.rng, self.cal)
            self.assertTrue(tamanhos_validos_clt(tams(ind), 30), tams(ind))
            self.assertGreater(calcular_fitness(ind, 30, self.cal), 0)   # inclui regra de início

    def test_ag_nao_piora_e_respeita_clt(self):
        for dias in (30, 10):
            res = executar_ag(self.cal, Parametros(max_geracoes=30, dias_ferias=dias), random.Random(7))
            self.assertGreaterEqual(res.historico_melhor[-1], res.historico_melhor[0])
            self.assertTrue(tamanhos_validos_clt(tams(res.melhor), dias))
            self.assertGreater(calcular_fitness(res.melhor, dias, self.cal), 0)


if __name__ == "__main__":
    unittest.main()
