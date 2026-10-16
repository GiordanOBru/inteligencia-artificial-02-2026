"""
kmeans_wholesale.py
===================
Ponto de entrada e compatibilidade para o agrupamento K-Means no Wholesale Customers.
Importa a arquitetura modularizada dos arquivos:
  - configuracoes.py
  - dados.py
  - modelo.py
  - analise.py
  - visualizacao.py
  - main.py
"""

from configuracoes import (
    ARQUIVO_SAIDA_PADRAO,
    ATRIBUTOS_CONSUMO,
    CAMINHO_DADOS_PADRAO,
    DIRETORIO_GRAFICOS_PADRAO,
    MAPA_CANAIS,
    MAPA_REGIOES,
)
from dados import carregar_dados, garantir_dados, preparar_dados
from modelo import avaliar_kmeans, treinar_modelo_final
from analise import analisar_clusters
from visualizacao import gerar_visualizacoes
from main import analisar_argumentos, executar_pipeline

# Alias para compatibilidade com nomes em inglês e português
ensure_dataset = carregar_dados
preprocess_data = preparar_dados
evaluate_kmeans_range = avaliar_kmeans
train_final_model = treinar_modelo_final
modelo_final = treinar_modelo_final
analyze_clusters = analisar_clusters
generate_visualizations = gerar_visualizacoes
run_pipeline = executar_pipeline
analise_args = analisar_argumentos

if __name__ == "__main__":
    args = analisar_argumentos()
    executar_pipeline(
        caminho_dados=args.caminho_dados,
        k_escolhido=args.k_escolhido,
        diretorio_saida=args.diretorio_saida,
        arquivo_saida=args.arquivo_saida,
        salvar_graficos=not args.sem_graficos,
    )
