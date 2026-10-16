"""
visualizacao.py
===============
Módulo de geração e exportação de gráficos de alta qualidade para o projeto K-Means.
Produz visualizações para métricas de validação e interpretação dos grupos.
"""

from __future__ import annotations

import os
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import StandardScaler

from configuracoes import configurar_estilo_graficos


def gerar_visualizacoes(
    df: pd.DataFrame,
    X_padronizado: np.ndarray,
    modelo: KMeans,
    resultados_avaliacao: Dict[str, object],
    atributos: List[str],
    diretorio_saida: str = "graficos",
) -> List[str]:
    """Gera e salva 5 figuras analíticas com alta resolução para documentação técnica e de negócio."""
    configurar_estilo_graficos()
    os.makedirs(diretorio_saida, exist_ok=True)
    arquivos_gerados = []

    k_valores = resultados_avaliacao["k_valores"]
    scores_silhueta = resultados_avaliacao["scores_silhueta"]
    inercias = resultados_avaliacao["inercias"]
    k_escolhido = modelo.n_clusters
    rotulos = modelo.labels_

    # 1. Gráfico Duplo: Curva de Silhueta e Método do Cotovelo
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Silhueta
    ax1.plot(k_valores, scores_silhueta, marker="o", color="#1f77b4", linewidth=2.5, markersize=8)
    ax1.axvline(k_escolhido, color="#d62728", linestyle="--", alpha=0.8, label=f"k Escolhido = {k_escolhido}")
    score_escolhido = scores_silhueta[k_valores.index(k_escolhido)]
    ax1.scatter([k_escolhido], [score_escolhido], color="#d62728", s=130, zorder=5)
    ax1.set_title("Coeficiente de Silhueta vs Número de Clusters (k)", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Número de Grupos (k)", fontsize=11)
    ax1.set_ylabel("Coeficiente de Silhueta Médio", fontsize=11)
    ax1.set_xticks(k_valores)
    ax1.legend()
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Inércia (Elbow)
    ax2.plot(k_valores, inercias, marker="s", color="#ff7f0e", linewidth=2.5, markersize=8)
    ax2.axvline(k_escolhido, color="#d62728", linestyle="--", alpha=0.8, label=f"k Escolhido = {k_escolhido}")
    ax2.set_title("Método do Cotovelo (Inércia / WCSS) vs k", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Número de Grupos (k)", fontsize=11)
    ax2.set_ylabel("Inércia (Within-Cluster Sum of Squares)", fontsize=11)
    ax2.set_xticks(k_valores)
    ax2.legend()
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    caminho_sil_elbow = os.path.join(diretorio_saida, "curva_silhueta_cotovelo.png")
    fig.savefig(caminho_sil_elbow, bbox_inches="tight")
    plt.close(fig)
    arquivos_gerados.append(caminho_sil_elbow)

    # 2. Projeção PCA em 2D com centróides
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_padronizado)
    centros_pca = pca.transform(modelo.cluster_centers_)
    var_explicada = pca.explained_variance_ratio_ * 100

    fig, ax = plt.subplots(figsize=(9, 6))
    scatter = ax.scatter(
        X_pca[:, 0],
        X_pca[:, 1],
        c=rotulos,
        cmap="tab10",
        alpha=0.75,
        edgecolors="none",
        s=45,
    )
    # Centróides
    ax.scatter(
        centros_pca[:, 0],
        centros_pca[:, 1],
        marker="X",
        s=200,
        c="black",
        edgecolors="white",
        linewidths=1.5,
        label="Centróides",
    )
    ax.set_title(
        f"Segmentação K-Means (k={k_escolhido}) Projetada em 2D via PCA",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xlabel(f"Componente Principal 1 ({var_explicada[0]:.1f}% da variância)", fontsize=11)
    ax.set_ylabel(f"Componente Principal 2 ({var_explicada[1]:.1f}% da variância)", fontsize=11)
    cbar = plt.colorbar(scatter, ax=ax, ticks=range(k_escolhido))
    cbar.set_label("Cluster")
    ax.legend(loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    caminho_pca = os.path.join(diretorio_saida, "clusters_pca_2d.png")
    fig.savefig(caminho_pca, bbox_inches="tight")
    plt.close(fig)
    arquivos_gerados.append(caminho_pca)

    # 3. Gráfico de Barras do Consumo Médio por Cluster
    medias_df = df.groupby("Cluster")[atributos].mean()
    fig, ax = plt.subplots(figsize=(11, 6))
    medias_df.T.plot(kind="bar", ax=ax, colormap="tab10", width=0.75)
    ax.set_title(
        f"Consumo Médio Anual por Categoria para Cada Cluster (k={k_escolhido})",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xlabel("Categoria de Produto", fontsize=11)
    ax.set_ylabel("Média Anual de Gastos (Unidades Monetárias)", fontsize=11)
    ax.legend(title="Cluster", title_fontsize="10")
    plt.xticks(rotation=20, ha="right")
    ax.grid(True, linestyle=":", alpha=0.6, axis="y")

    plt.tight_layout()
    caminho_barras = os.path.join(diretorio_saida, "perfil_consumo_clusters.png")
    fig.savefig(caminho_barras, bbox_inches="tight")
    plt.close(fig)
    arquivos_gerados.append(caminho_barras)

    # 4. Heatmap de Consumo Médio Normalizado (Z-Score)
    escalonador_medias = StandardScaler()
    medias_padronizadas = pd.DataFrame(
        escalonador_medias.fit_transform(medias_df),
        index=[f"Cluster {i}" for i in medias_df.index],
        columns=atributos,
    )

    fig, ax = plt.subplots(figsize=(9, 4.5))
    sns.heatmap(
        medias_padronizadas,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.8,
        cbar_kws={"label": "Desvios Padronizados (Z-Score)"},
        ax=ax,
    )
    ax.set_title(
        f"Heatmap de Intensidade Relativa de Consumo por Cluster (k={k_escolhido})",
        fontsize=12,
        fontweight="bold",
    )
    plt.xticks(rotation=20, ha="right")

    plt.tight_layout()
    caminho_heatmap = os.path.join(diretorio_saida, "heatmap_consumo_normalizado.png")
    fig.savefig(caminho_heatmap, bbox_inches="tight")
    plt.close(fig)
    arquivos_gerados.append(caminho_heatmap)

    # 5. Silhouette Plot Individual das Amostras
    silhuetas_amostras = silhouette_samples(X_padronizado, rotulos)
    fig, ax = plt.subplots(figsize=(9, 6))
    y_inferior = 10

    for i in range(k_escolhido):
        valores_silhueta_i = silhuetas_amostras[rotulos == i]
        valores_silhueta_i.sort()
        tamanho_cluster_i = valores_silhueta_i.shape[0]
        y_superior = y_inferior + tamanho_cluster_i

        cor = plt.cm.tab10(float(i) / 10)
        ax.fill_betweenx(
            np.arange(y_inferior, y_superior),
            0,
            valores_silhueta_i,
            facecolor=cor,
            edgecolor=cor,
            alpha=0.7,
        )
        ax.text(-0.05, y_inferior + 0.5 * tamanho_cluster_i, f"C{i}")
        y_inferior = y_superior + 10

    silhueta_media = silhouette_score(X_padronizado, rotulos)
    ax.axvline(
        x=silhueta_media,
        color="red",
        linestyle="--",
        label=f"Silhueta Média = {silhueta_media:.4f}",
    )
    ax.set_title(
        f"Análise de Silhueta Amostra a Amostra para k={k_escolhido}",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xlabel("Valores do Coeficiente de Silhueta", fontsize=11)
    ax.set_ylabel("Rótulo do Cluster (Amostras ordenadas)", fontsize=11)
    ax.set_yticks([])
    ax.set_xlim([-0.2, 1.0])
    ax.legend(loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    caminho_sil_plot = os.path.join(diretorio_saida, "distribuicao_silhueta_amostras.png")
    fig.savefig(caminho_sil_plot, bbox_inches="tight")
    plt.close(fig)
    arquivos_gerados.append(caminho_sil_plot)

    print(f"\n[SUCESSO] 5 gráficos gerados e salvos no diretório '{diretorio_saida}/':")
    for f in arquivos_gerados:
        print(f"  - {f}")

    return arquivos_gerados
