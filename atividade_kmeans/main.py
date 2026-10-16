"""
Ponto de entrada principal do projeto de Agrupamento K-Means no Wholesale Customers.
Orquestra o pipeline completo através dos módulos especializados.
"""

from __future__ import annotations

import argparse
import pandas as pd

from analise import analisar_clusters
from configuracoes import (
    ARQUIVO_SAIDA_PADRAO,
    ATRIBUTOS_CONSUMO,
    CAMINHO_DADOS_PADRAO,
    DIRETORIO_GRAFICOS_PADRAO,
)
from dados import carregar_dados, garantir_dados, preparar_dados
from modelo import avaliar_kmeans, treinar_modelo_final
from visualizacao import gerar_visualizacoes


def executar_pipeline(
    caminho_dados: str = CAMINHO_DADOS_PADRAO,
    k_escolhido: int | None = None,
    diretorio_saida: str = DIRETORIO_GRAFICOS_PADRAO,
    arquivo_saida: str = ARQUIVO_SAIDA_PADRAO,
    salvar_graficos: bool = True,
) -> pd.DataFrame:
    """Orquestra o fluxo de ponta a ponta: carga, pré-processamento, otimização, modelagem, análise e gráficos."""
    print("=" * 65)
    print("INICIANDO PIPELINE: CLUSTERING K-MEANS NO WHOLESALE CUSTOMERS")
    print("=" * 65)

    # 1. Carregar dataset local
    df = carregar_dados(caminho_dados)

    # 2. Pré-processar e normalizar atributos de consumo
    _, X_padronizado, _ = preparar_dados(df, ATRIBUTOS_CONSUMO)

    # 3. Avaliar k de 2 a 10 com Silhouette Score
    resultados_avaliacao = avaliar_kmeans(X_padronizado, k_min=2, k_max=10)

    # 4. Definir k (automático via silhueta ou definido pelo usuário)
    k_final = k_escolhido if k_escolhido is not None else resultados_avaliacao["melhor_k"]
    if k_escolhido is not None:
        print(f"\n[INFO] Utilizando k={k_escolhido} definido manualmente pelo usuário.")
    else:
        print(f"\n[INFO] Utilizando k={k_final} selecionado automaticamente pelo melhor Silhouette Score.")

    # 5. Treinar modelo definitivo
    modelo, rotulos = treinar_modelo_final(X_padronizado, k=k_final)
    df["Cluster"] = rotulos

    # 6. Analisar perfis dos grupos gerados
    analisar_clusters(df, ATRIBUTOS_CONSUMO, coluna_cluster="Cluster")

    # 7. Gerar gráficos se habilitado
    if salvar_graficos:
        gerar_visualizacoes(
            df=df,
            X_padronizado=X_padronizado,
            modelo=modelo,
            resultados_avaliacao=resultados_avaliacao,
            atributos=ATRIBUTOS_CONSUMO,
            diretorio_saida=diretorio_saida,
        )

    # 8. Exportar dataset enriquecido com a coluna Cluster
    df.to_csv(arquivo_saida, index=False)
    print(f"\n[SUCESSO] Dataset enriquecido salvo em: '{arquivo_saida}'")
    print("=" * 65)
    print("PIPELINE CONCLUÍDO COM ÊXITO!")
    print("=" * 65)

    return df


def analisar_argumentos():
    """Configura e processa argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Pipeline K-Means com Coeficiente de Silhueta no dataset Wholesale Customers."
    )
    parser.add_argument(
        "--dados",
        "--data-path",
        dest="caminho_dados",
        type=str,
        default=CAMINHO_DADOS_PADRAO,
        help="Caminho do arquivo CSV de entrada.",
    )
    parser.add_argument(
        "--k",
        dest="k_escolhido",
        type=int,
        default=None,
        help="Valor específico de k para treinar o modelo. Se omitido, usa o k ideal pelo Silhouette Score.",
    )
    parser.add_argument(
        "--graficos",
        "--output-dir",
        dest="diretorio_saida",
        type=str,
        default=DIRETORIO_GRAFICOS_PADRAO,
        help="Diretório onde os gráficos gerados serão salvos.",
    )
    parser.add_argument(
        "--saida",
        "--output-csv",
        dest="arquivo_saida",
        type=str,
        default=ARQUIVO_SAIDA_PADRAO,
        help="Caminho do CSV de saída com os clusters atribuídos.",
    )
    parser.add_argument(
        "--sem-graficos",
        "--no-plots",
        dest="sem_graficos",
        action="store_true",
        help="Desativa a geração e salvamento dos gráficos.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = analisar_argumentos()
    executar_pipeline(
        caminho_dados=args.caminho_dados,
        k_escolhido=args.k_escolhido,
        diretorio_saida=args.diretorio_saida,
        arquivo_saida=args.arquivo_saida,
        salvar_graficos=not args.sem_graficos,
    )
