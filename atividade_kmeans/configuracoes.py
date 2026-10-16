"""
Módulo de configurações e constantes para o projeto K-Means Wholesale.
Centraliza caminhos de arquivos, URLs, parâmetros estéticos e variáveis de consumo.
"""

import sys
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração de encoding UTF-8 para exibição correta de acentos em terminais Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Caminhos padrão dos arquivos
CAMINHO_DADOS_PADRAO = "customer_dados.csv"
DIRETORIO_GRAFICOS_PADRAO = "graficos"
ARQUIVO_SAIDA_PADRAO = "dados_customers_clustered.csv"

# Variáveis contínuas de gastos anuais (em unidades monetárias)
ATRIBUTOS_CONSUMO = [
    "Fresh",
    "Milk",
    "Grocery",
    "Frozen",
    "Detergents_Paper",
    "Delicassen",
]

# Mapeamentos para interpretação de variáveis contextuais
MAPA_CANAIS = {
    1: "Horeca (Hotel/Restaurante/Café)",
    2: "Retail (Varejo)",
}

MAPA_REGIOES = {
    1: "Lisboa",
    2: "Porto",
    3: "Outras Regiões",
}


def configurar_estilo_graficos():
    """Aplica o tema visual e definições tipográficas para gráficos de alta qualidade."""
    sns.set_theme(style="whitegrid", palette="deep")
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["figure.dpi"] = 150
