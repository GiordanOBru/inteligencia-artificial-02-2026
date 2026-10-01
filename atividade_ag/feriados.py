"""
MÓDULO 1 - DADOS & REPRESENTAÇÃO GENÉTICA                      (Responsável: Aluno A)
-----------------------------------------------------------------------------------
- Calendário anual (365/366 dias) com feriados federais, estaduais (TO) e
  municipais (Palmas).
- Estruturas: Individuo (cromossomo + aptidão) e População.
- Regras da CLT: fracionamento (até 3 períodos; um >= 14 dias; demais >= 5) e
  início das férias (art. 134 §3º: não nos 2 dias antes de feriado/domingo).

Convenção: os índices Python são 0-based. O gene i corresponde ao dia i+1 do ano
(i = 0 -> 1º de janeiro).
"""
import random
from dataclasses import dataclass, field
from datetime import date, timedelta

UF = "TO"
MUNICIPIO = "Palmas"

# Níveis de feriado
MUNICIPAL, ESTADUAL, FEDERAL = "MUNICIPAL", "ESTADUAL", "FEDERAL"


# ----------------------------------------------------------------------------
# Feriados
# ----------------------------------------------------------------------------
def calcular_pascoa(ano: int) -> date:
    """Domingo de Páscoa (algoritmo gregoriano anônimo)."""
    a, b, c = ano % 19, ano // 100, ano % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return date(ano, mes, dia)


def pontos_facultativos(ano: int) -> dict:
    """Não são feriados por lei: a folga depende do empregador/convenção coletiva.
    Por padrão NÃO são tratados como folga (ver Calendario)."""
    pascoa = calcular_pascoa(ano)
    return {
        pascoa - timedelta(days=48): "Carnaval (segunda) - ponto facultativo",
        pascoa - timedelta(days=47): "Carnaval (terça) - ponto facultativo",
        pascoa + timedelta(days=60): "Corpus Christi - ponto facultativo",
    }


def feriados_federais(ano: int) -> dict:
    pascoa = calcular_pascoa(ano)
    return {
        date(ano, 1, 1): "Confraternização Universal",
        pascoa - timedelta(days=2): "Sexta-feira Santa",
        date(ano, 4, 21): "Tiradentes",
        date(ano, 5, 1): "Dia do Trabalhador",
        date(ano, 9, 7): "Independência do Brasil",
        date(ano, 10, 12): "Nossa Senhora Aparecida",
        date(ano, 11, 2): "Finados",
        date(ano, 11, 15): "Proclamação da República",
        date(ano, 11, 20): "Consciência Negra",
        date(ano, 12, 25): "Natal",
    }


def feriados_estaduais_to(ano: int) -> dict:
    return {
        date(ano, 3, 18): "Autonomia do Estado do Tocantins",
        date(ano, 9, 8): "N. Sra. da Natividade (padroeira do TO)",
        date(ano, 10, 5): "Criação do Estado do Tocantins",
    }


def feriados_municipais_palmas(ano: int) -> dict:
    # ATENÇÃO: confirmar na legislação municipal vigente antes do uso real.
    return {
        date(ano, 5, 20): "Aniversário de Palmas",
        date(ano, 12, 8): "N. Sra. da Consolação (padroeira de Palmas)",
    }


# ----------------------------------------------------------------------------
# Calendário
# ----------------------------------------------------------------------------
class Calendario:
    """Mapeia os dias do ano e responde 'que tipo de dia é este?'."""

    def __init__(self, ano: int, incluir_facultativos: bool = False):
        self.ano = ano
        inicio = date(ano, 1, 1)
        self.total_dias = (date(ano + 1, 1, 1) - inicio).days  # 365 (ou 366)
        self.dias = [inicio + timedelta(days=i) for i in range(self.total_dias)]

        # Prioridade em caso de datas coincidentes: municipal > estadual > federal
        self._feriados = {}
        for nivel, fonte in (
            (FEDERAL, pontos_facultativos(ano) if incluir_facultativos else {}),
            (FEDERAL, feriados_federais(ano)),
            (ESTADUAL, feriados_estaduais_to(ano)),
            (MUNICIPAL, feriados_municipais_palmas(ano)),
        ):
            for d, nome in fonte.items():
                self._feriados[d] = (nivel, nome)

    # --- consultas por índice do gene ---
    def eh_feriado_municipal(self, i: int) -> bool:
        return self._feriados.get(self.dias[i], (None,))[0] == MUNICIPAL

    def eh_feriado_estadual(self, i: int) -> bool:
        return self._feriados.get(self.dias[i], (None,))[0] == ESTADUAL

    def eh_feriado_federal(self, i: int) -> bool:
        return self._feriados.get(self.dias[i], (None,))[0] == FEDERAL

    def eh_fim_de_semana(self, i: int) -> bool:
        return self.dias[i].weekday() >= 5

    def eh_folga(self, i: int) -> bool:
        """Dia em que já não se trabalha: fim de semana ou qualquer feriado."""
        return self.eh_fim_de_semana(i) or self.dias[i] in self._feriados

    def eh_feriado(self, i: int) -> bool:
        return self.dias[i] in self._feriados

    def inicio_permitido(self, i: int) -> bool:
        """CLT art. 134 §3º: é vedado iniciar as férias nos 2 dias que antecedem
        feriado ou repouso semanal (domingo). Por cautela, também não se inicia
        no próprio dia do feriado/domingo (Precedente Normativo 100 do TST)."""
        for k in range(3):
            d = self.dias[0] + timedelta(days=i + k)
            if d.weekday() == 6 or d in self._feriados or (d.month == 1 and d.day == 1):
                return False
        return True

    def nome_feriado(self, i: int):
        info = self._feriados.get(self.dias[i])
        return info[1] if info else None


# ----------------------------------------------------------------------------
# Regras da CLT para fracionamento das férias (art. 134)
#   - até 3 períodos;
#   - um deles com no mínimo 14 dias corridos;
#   - os demais com no mínimo 5 dias corridos cada.
# Se o total for < 19 dias (ex.: 10 ou 6), não há como fracionar respeitando a
# regra, então o único formato aceito é UM período contínuo.
# ----------------------------------------------------------------------------
MAX_PERIODOS = 3
MIN_PERIODO_PRINCIPAL = 14
MIN_PERIODO_DEMAIS = 5


def minimos_por_periodo(k: int, dias: int) -> list:
    """Tamanhos mínimos para k períodos (o 1º é o 'principal')."""
    return [min(MIN_PERIODO_PRINCIPAL, dias)] + [MIN_PERIODO_DEMAIS] * (k - 1)


def max_periodos_permitidos(dias: int) -> int:
    if dias < MIN_PERIODO_PRINCIPAL + MIN_PERIODO_DEMAIS:
        return 1
    k = 1
    while k < MAX_PERIODOS and sum(minimos_por_periodo(k + 1, dias)) <= dias:
        k += 1
    return k


def tamanhos_validos_clt(tamanhos: list, dias: int) -> bool:
    """Valida a lista de tamanhos dos períodos contra a regra da CLT."""
    if not tamanhos or sum(tamanhos) != dias:
        return False
    if len(tamanhos) > max_periodos_permitidos(dias):
        return False
    if len(tamanhos) == 1:
        return True
    return max(tamanhos) >= MIN_PERIODO_PRINCIPAL and all(t >= MIN_PERIODO_DEMAIS for t in tamanhos)


def blocos_contiguos(cromossomo: list) -> list:
    """Lista de (indice_inicial, tamanho) de cada bloco contínuo de 1s."""
    blocos, i, n = [], 0, len(cromossomo)
    while i < n:
        if cromossomo[i] == 1:
            j = i
            while j + 1 < n and cromossomo[j + 1] == 1:
                j += 1
            blocos.append((i, j - i + 1))
            i = j + 1
        else:
            i += 1
    return blocos


def posicionar_blocos(tamanhos: list, n_dias: int, rng: random.Random,
                      preferidos=None, permitido=None):
    """Coloca blocos no calendário sem sobreposição e com >= 1 dia de intervalo
    entre eles (para não se fundirem). `preferidos` = inícios desejados (opcional);
    `permitido(ini)` = restrição sobre o dia de início (CLT art. 134 §3º).
    Devolve o cromossomo ou None se não couber."""
    c = [0] * n_dias

    def livre(ini, tam):
        return not any(c[max(0, ini - 1):min(n_dias, ini + tam + 1)])

    def ok(ini):
        return permitido is None or permitido(ini)

    ordem = list(range(len(tamanhos)))
    rng.shuffle(ordem)
    for idx in ordem:
        tam = tamanhos[idx]
        ini = None
        if preferidos is not None:
            p = min(max(preferidos[idx], 0), n_dias - tam)
            if livre(p, tam) and ok(p):
                ini = p
        if ini is None:
            candidatos = [s for s in range(n_dias - tam + 1) if livre(s, tam) and ok(s)]
            if not candidatos:
                return None
            if preferidos is not None:          # mantém a posição aproximada
                candidatos.sort(key=lambda s: abs(s - preferidos[idx]))
                candidatos = candidatos[:5]
            ini = rng.choice(candidatos)
        for d in range(ini, ini + tam):
            c[d] = 1
    return c


# ----------------------------------------------------------------------------
# Estruturas genéticas
# ----------------------------------------------------------------------------
@dataclass
class Individuo:
    cromossomo: list                 # vetor binário: 1 = férias, 0 = dia normal
    aptidao: float = field(default=0.0)

    def copia(self) -> "Individuo":
        return Individuo(self.cromossomo[:], self.aptidao)


def composicao_aleatoria(dias: int, k: int, rng: random.Random) -> list:
    """Tamanhos aleatórios de k períodos que respeitam a CLT."""
    if k == 1:
        return [dias]
    tam = minimos_por_periodo(k, dias)
    for _ in range(dias - sum(tam)):
        tam[rng.randrange(k)] += 1
    return tam


def gerar_individuo_aleatorio(n_dias: int, dias_ferias: int, rng: random.Random,
                              calendario=None) -> Individuo:
    """Indivíduo factível: `dias_ferias` dias, em até 3 períodos válidos (CLT),
    com início permitido (art. 134 §3º) quando `calendario` é informado."""
    permitido = calendario.inicio_permitido if calendario is not None else None
    for _ in range(100):
        k = rng.randint(1, max_periodos_permitidos(dias_ferias))
        tam = composicao_aleatoria(dias_ferias, k, rng)
        c = posicionar_blocos(tam, n_dias, rng, permitido=permitido)
        if c is not None:
            return Individuo(c)
    raise RuntimeError("Não foi possível gerar um indivíduo válido.")


def gerar_populacao_inicial(tamanho: int, n_dias: int, dias_ferias: int,
                            rng: random.Random, calendario=None) -> list:
    return [gerar_individuo_aleatorio(n_dias, dias_ferias, rng, calendario)
            for _ in range(tamanho)]


# ----------------------------------------------------------------------------
# Decodificação (cromossomo -> datas)
# ----------------------------------------------------------------------------
def converter_cromossomo_para_datas(cromossomo: list, calendario: Calendario) -> list:
    return [calendario.dias[i] for i, g in enumerate(cromossomo) if g == 1]


def agrupar_periodos(cromossomo: list, calendario: Calendario) -> list:
    """Devolve lista de (inicio, fim, qtd_dias) para cada bloco contínuo."""
    return [(calendario.dias[i], calendario.dias[i + t - 1], t)
            for i, t in blocos_contiguos(cromossomo)]
