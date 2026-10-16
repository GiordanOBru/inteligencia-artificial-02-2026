"""
Módulo de análise descritiva e mercadológica dos clusters gerados pelo K-Means.
Calcula estatísticas de consumo e cruza com canais e regiões geográficas.
"""

from __future__ import annotations

from typing import Dict, List

import pandas as pd

from configuracoes import MAPA_CANAIS, MAPA_REGIOES


def analisar_clusters(
    df: pd.DataFrame, atributos: List[str], coluna_cluster: str = "Cluster"
) -> Dict[str, pd.DataFrame]:
    """Gera tabelas de caracterização dos clusters: contagem, médias, medianas e correlação com canais/regiões."""
    total_clientes = len(df)
    contagens = df[coluna_cluster].value_counts().sort_index()
    percentuais = (contagens / total_clientes) * 100

    distribuicao = pd.DataFrame(
        {"Contagem": contagens, "Percentual (%)": percentuais.round(2)}
    )

    medias = df.groupby(coluna_cluster)[atributos].mean().round(2)
    medianas = df.groupby(coluna_cluster)[atributos].median().round(2)

    # Análise cruzada com Channel (Canal)
    cruzamento_canal = None
    if "Channel" in df.columns:
        series_canal = df["Channel"].map(MAPA_CANAIS)
        cruzamento_canal = pd.crosstab(
            df[coluna_cluster], series_canal, normalize="index"
        ).round(4) * 100

    # Análise cruzada com Region (Região)
    cruzamento_regiao = None
    if "Region" in df.columns:
        series_regiao = df["Region"].map(MAPA_REGIOES)
        cruzamento_regiao = pd.crosstab(
            df[coluna_cluster], series_regiao, normalize="index"
        ).round(4) * 100

    print("\n" + "=" * 65)
    print(f"{'DISTRIBUIÇÃO DOS CLIENTES POR CLUSTER':^65}")
    print("=" * 65)
    print(distribuicao.to_string())

    print("\n" + "=" * 65)
    print(f"{'PERFIL MÉDIO DE CONSUMO POR CLUSTER (Unidades Monetárias)':^65}")
    print("=" * 65)
    print(medias.to_string())

    print("\n" + "=" * 65)
    print(f"{'PERFIL MEDIANO DE CONSUMO POR CLUSTER (Unidades Monetárias)':^65}")
    print("=" * 65)
    print(medianas.to_string())

    if cruzamento_canal is not None:
        print("\n" + "=" * 65)
        print(f"{'COMPOSIÇÃO DE CANAIS POR CLUSTER (%)':^65}")
        print("=" * 65)
        print(cruzamento_canal.to_string())

    if cruzamento_regiao is not None:
        print("\n" + "=" * 65)
        print(f"{'COMPOSIÇÃO DE REGIÕES POR CLUSTER (%)':^65}")
        print("=" * 65)
        print(cruzamento_regiao.to_string())

    return {
        "distribuicao": distribuicao,
        "medias": medias,
        "medianas": medianas,
        "cruzamento_canal": cruzamento_canal,
        "cruzamento_regiao": cruzamento_regiao,
    }
