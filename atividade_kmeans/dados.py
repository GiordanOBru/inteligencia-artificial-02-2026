"""
Módulo responsável pelo carregamento e pré-processamento dos dados dos clientes.
"""

from __future__ import annotations

import os
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from configuracoes import CAMINHO_DADOS_PADRAO


def carregar_dados(caminho_arquivo: str = CAMINHO_DADOS_PADRAO) -> pd.DataFrame:
    """Carrega o arquivo CSV local com os dados dos clientes."""
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(
            f"[ERRO] O arquivo esperado '{caminho_arquivo}' não foi encontrado. "
            f"Certifique-se de que ele está presente na pasta do projeto para execução."
        )

    df = pd.read_csv(caminho_arquivo)
    print(f"[OK] Dados carregados com sucesso de '{caminho_arquivo}': {df.shape[0]} linhas e {df.shape[1]} colunas.")
    return df


# Alias para compatibilidade
garantir_dados = carregar_dados


def preparar_dados(
    dados_df: pd.DataFrame, atributos: List[str]
) -> Tuple[pd.DataFrame, np.ndarray, StandardScaler]:
    """Valida valores ausentes, extrai os atributos contínuos e aplica padronização StandardScaler.
    
    Retorna:
        - X: DataFrame com os dados brutos dos atributos de consumo selecionados.
        - X_padronizado: Matriz NumPy padronizada (média 0, desvio padrão 1).
        - escalonador: O objeto StandardScaler ajustado.
    """
    # Verificar valores ausentes nas colunas numéricas
    valores_nulos = dados_df[atributos].isnull().sum().sum()
    if valores_nulos > 0:
        print(f"[AVISO] Encontrados {valores_nulos} valores ausentes. Preenchendo com a mediana.")
        X = dados_df[atributos].fillna(dados_df[atributos].median())
    else:
        X = dados_df[atributos].copy()

    # Aplicação do StandardScaler (Z-Score)
    escalonador = StandardScaler()
    X_padronizado = escalonador.fit_transform(X)

    return X, X_padronizado, escalonador
