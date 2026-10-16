"""
Módulo de modelagem matemática do algoritmo K-Means.
Contém a busca do número ideal de clusters através do Coeficiente de Silhueta
e o treinamento do modelo definitivo.
"""

from __future__ import annotations

from typing import Dict, Tuple

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def avaliar_kmeans(
    X_padronizado: np.ndarray,
    k_min: int = 2,
    k_max: int = 10,
    random_state: int = 42,
) -> Dict[str, object]:
    """Executa o K-Means para um intervalo de k e calcula o Coeficiente de Silhueta e a Inércia (WCSS).
    
    Retorna um dicionário contendo as métricas de cada iteração e o k ótimo identificado.
    """
    k_valores = list(range(k_min, k_max + 1))
    scores_silhueta = []
    inercias = []

    print("\n" + "=" * 65)
    print(f"{'AVALIAÇÃO DE HIPERPARÂMETRO K (K-MEANS)':^65}")
    print("=" * 65)
    print(f"{'k':>4} | {'Coeficiente de Silhueta':^26} | {'Inércia (WCSS)':^24}")
    print("-" * 65)

    for k in k_valores:
        kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        rotulos = kmeans.fit_predict(X_padronizado)
        score_atual = silhouette_score(X_padronizado, rotulos)
        inercia_atual = kmeans.inertia_

        scores_silhueta.append(score_atual)
        inercias.append(inercia_atual)

        print(f"{k:>4} | {score_atual:^26.4f} | {inercia_atual:^24.2f}")

    print("-" * 65)

    melhor_indice = int(np.argmax(scores_silhueta))
    melhor_k = k_valores[melhor_indice]
    melhor_score = scores_silhueta[melhor_indice]

    print(f"\n[RECOMENDAÇÃO] k ideal pelo Coeficiente de Silhueta: k = {melhor_k} (Score: {melhor_score:.4f})")

    return {
        "k_valores": k_valores,
        "scores_silhueta": scores_silhueta,
        "inercias": inercias,
        "melhor_k": melhor_k,
        "melhor_score": melhor_score,
    }


def treinar_modelo_final(
    X_padronizado: np.ndarray, k: int, random_state: int = 42
) -> Tuple[KMeans, np.ndarray]:
    """Treina o modelo K-Means final com o valor selecionado de k.
    
    Retorna a tupla (modelo_kmeans, rotulos_clusters).
    """
    modelo = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    rotulos = modelo.fit_predict(X_padronizado)
    return modelo, rotulos
