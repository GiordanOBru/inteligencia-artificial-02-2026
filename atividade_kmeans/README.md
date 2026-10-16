# Agrupamento K-Means no Dataset Wholesale Customers com Coeficiente de Silhueta

Projeto da disciplina de Inteligência Artificial / Aprendizado de Máquina — Universidade Federal do Tocantins (UFT).

**Professor:** Alexandre Tadeu Rossini da Silva

**Integrantes:**
- Maria Luiza Pinheiro Higashi
- Giordano Bruno de Moura Fragoso Santos

## Descrição

Aplicação do algoritmo **K-Means** (aprendizado não supervisionado) ao conjunto de dados **Wholesale Customers** (UCI Machine Learning Repository) para segmentar os **440 clientes** de um distribuidor atacadista em grupos de consumo distintos. O número ideal de grupos (k) é escolhido pelo **Coeficiente de Silhueta**.

O projeto busca:

- Identificar padrões de consumo anual entre os clientes
- Determinar automaticamente o melhor valor de k no intervalo [2, 10]
- Caracterizar cada grupo (consumo médio, canal de venda e região)
- Sugerir ações de negócio para cada perfil encontrado

## Modelagem

- **Entrada:** 6 variáveis contínuas de consumo anual: `Fresh`, `Milk`, `Grocery`, `Frozen`, `Detergents_Paper` e `Delicassen`.
- **Pré-processamento:** padronização Z-Score (`StandardScaler`), necessária porque o K-Means usa distância Euclidiana e as variáveis têm escalas muito diferentes. Valores ausentes são imputados pela mediana.
- **Função objetivo:** minimizar a inércia (WCSS), a soma dos quadrados das distâncias de cada ponto ao centróide do seu cluster.
- **Escolha de k:** o k com maior Coeficiente de Silhueta médio, s(i) = (b(i) − a(i)) / max(a(i), b(i)), em que a(i) é a coesão intra-cluster e b(i) é a separação para o cluster vizinho mais próximo.

## Parâmetros do Modelo

| Parâmetro | Valor |
|---|---|
| Algoritmo | K-Means (scikit-learn) |
| Intervalo testado para k | 2 a 10 |
| Métrica de seleção | Coeficiente de Silhueta médio |
| Métrica auxiliar | Inércia (WCSS) |
| Padronização | StandardScaler (Z-Score) |
| Semente aleatória | `random_state = 42` |
| Número de atributos | 6 variáveis de consumo |
| Número de amostras | 440 clientes |

## Resultados

### Avaliação de k

| k | Silhueta médio | Inércia (WCSS) |
|:---:|:---:|:---:|
| 2 | 0,5472 | 1956,12 |
| **3** | **0,5483** | **1608,43** |
| 4 | 0,3485 | 1317,84 |
| 5 | 0,3690 | 1058,77 |
| 6 | 0,3782 | 915,74 |
| 7 | 0,3343 | 825,40 |
| 8 | 0,3201 | 737,39 |
| 9 | 0,3090 | 661,45 |
| 10 | 0,3112 | 605,92 |

O melhor valor é **k = 3**, com Silhueta de **0,5483**.

### Perfil dos grupos (k = 3)

| Atributo (média anual) | Cluster 0 | Cluster 1 | Cluster 2 |
|---|:---:|:---:|:---:|
| Fresh | 10.440,93 | 12.062,91 | 34.782,00 |
| Milk | 19.386,42 | 4.115,10 | 30.367,00 |
| Grocery | 28.656,09 | 5.534,97 | 16.898,00 |
| Frozen | 2.190,24 | 2.940,68 | 48.701,50 |
| Detergents_Paper | 13.327,80 | 1.696,17 | 755,50 |
| Delicassen | 2.374,20 | 1.299,11 | 26.776,00 |
| **Clientes** | 45 (10,23%) | 393 (89,32%) | 2 (0,45%) |
| **Canal dominante** | 97,78% Retail | 75,06% Horeca | 100% Horeca |

### Interpretação dos grupos

| Cluster | Persona | Ação de negócio sugerida |
|---|---|---|
| 0 | Redes de varejo, supermercados e mercearias | Fidelização no atacado de secos e molhados, logística para embalagens grandes, descontos em volume |
| 1 | Restaurantes e cafés de pequeno e médio porte | Entregas frequentes de perecíveis, pedidos recorrentes por aplicativo, promoções sazonais |
| 2 | Grandes compradores (hotéis de luxo e frigoríficos) | Atendimento "Key Account", contratos anuais personalizados, garantia de suprimento |

## Visualizações geradas

Salvas automaticamente na pasta `graficos/`:

| Arquivo | Conteúdo |
|---|---|
| `curva_silhueta_cotovelo.png` | Silhueta e inércia para k = 2 a 10, com destaque em k = 3 |
| `clusters_pca_2d.png` | Projeção PCA 2D dos clusters e centróides |
| `perfil_consumo_clusters.png` | Consumo médio por categoria em cada cluster |
| `heatmap_consumo_normalizado.png` | Mapa de calor Z-Score das médias por cluster |
| `distribuicao_silhueta_amostras.png` | Silhouette Plot amostra a amostra do modelo final |

## Pré-requisitos

- Python 3.10 ou superior
- pip

```bash
python --version
```

## Como executar

```bash
git clone https://github.com/usuario/kmeans-wholesale-customers.git
cd kmeans-wholesale-customers
pip install -r requirements.txt
python main.py
```

Opções de linha de comando:

| Opção | Descrição |
|---|---|
| `--k 2` | Força um número específico de clusters |
| `--dados caminho.csv` | Define o dataset de entrada |
| `--saida arquivo.csv` | Define o CSV de saída com a coluna `Cluster` |
| `--graficos pasta/` | Define a pasta dos gráficos |
| `--sem-graficos` | Executa apenas a saída textual e o CSV |
| `--help` | Exibe o menu de ajuda |

## Estrutura do projeto

```text
atividade_kmeans/
│
├── main.py
├── kmeans_wholesale.py
├── configuracoes.py
├── dados.py
├── modelo.py
├── analise.py
├── visualizacao.py
├── customer_dados.csv
├── dados_customers_clustered.csv
├── planejamento_kmeans_wholesale.md
├── README.md
├── requirements.txt
└── graficos/
```

| Módulo | Função |
|---|---|
| `configuracoes.py` | Caminhos, constantes, mapeamento de Canal/Região e estilo dos gráficos |
| `dados.py` | `carregar_dados` e `preparar_dados` (imputação e StandardScaler) |
| `modelo.py` | `avaliar_kmeans` (varredura de k, Silhueta e Inércia) e `treinar_modelo_final` |
| `analise.py` | `analisar_clusters` (contagens, médias, medianas e cruzamento com Canal/Região) |
| `visualizacao.py` | `gerar_visualizacoes` (5 gráficos em alta resolução) |
| `main.py` | `executar_pipeline` e `analisar_argumentos` (CLI) |
| `kmeans_wholesale.py` | Wrapper de compatibilidade com `main.py` |

## Testes

O projeto é validado verificando:

- Carga correta do dataset (440 linhas e 6 atributos de consumo)
- Tratamento de valores ausentes e padronização (média ≈ 0 e desvio ≈ 1)
- Varredura de k de 2 a 10 com Silhueta e Inércia calculadas para cada valor
- Seleção automática do k de maior Silhueta (k = 3)
- Consistência das contagens por cluster (soma igual a 440)
- Geração dos 5 gráficos e do CSV `dados_customers_clustered.csv`
- Funcionamento das opções de linha de comando (`--k`, `--dados`, `--saida`, `--graficos`, `--sem-graficos`)

## Divisão de trabalho

| Integrante | Responsabilidades |
|---|---|
| Maria Luiza Pinheiro Higashi | Configurações globais (`configuracoes.py`); carga, tratamento e padronização dos dados (`dados.py`); modelagem do K-Means, varredura de k e cálculo do Coeficiente de Silhueta e da Inércia (`modelo.py`); fundamentação teórica |
| Giordano Bruno de Moura Fragoso Santos | Análise descritiva e cruzamento com Canal/Região (`analise.py`); interpretação das personas de negócio; geração dos 5 gráficos (`visualizacao.py`); orquestração do pipeline, CLI e exportação do CSV (`main.py` e `kmeans_wholesale.py`) |