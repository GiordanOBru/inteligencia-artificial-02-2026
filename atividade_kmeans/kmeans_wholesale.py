"""
Ponto de entrada para o agrupamento K-Means no Wholesale Customers.
Importa a arquitetura modularizada dos arquivos:
  - configuracoes.py
  - dados.py
  - modelo.py
  - analise.py
  - visualizacao.py
  - main.py
"""

from analise import analisar_clusters
from configuracoes import (
    ARQUIVO_SAIDA_PADRAO,
    ATRIBUTOS_CONSUMO,
    CAMINHO_DADOS_PADRAO,
    DIRETORIO_GRAFICOS_PADRAO,
    MAPA_CANAIS,
    MAPA_REGIOES,
)
from dados import carregar_dados, garantir_dados, preparar_dados
from main import analisar_argumentos, executar_pipeline
from modelo import avaliar_kmeans, treinar_modelo_final
from visualizacao import gerar_visualizacoes

if __name__ == "__main__":
    args = analisar_argumentos()
    executar_pipeline(
        caminho_dados=args.caminho_dados,
        k_escolhido=args.k_escolhido,
        diretorio_saida=args.diretorio_saida,
        arquivo_saida=args.arquivo_saida,
        salvar_graficos=not args.sem_graficos,
    )
