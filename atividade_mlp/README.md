# Regressão com Rede Neural MLP no Dataset Video Game Sales

Projeto da disciplina de Inteligência Artificial / Aprendizado de Máquina — Universidade Federal do Tocantins (UFT).

**Professor:** Alexandre Tadeu Rossini da Silva

**Integrantes:**
- Maria Luiza Pinheiro Higashi
- Giordano Bruno de Moura Fragoso Santos

## Descrição

Aplicação de aprendizado supervisionado (**Regressão**) com **Rede Neural Perceptron Multicamadas (`MLPRegressor`)** do Scikit-Learn para estimar as vendas globais de jogos eletrônicos (`Global_Sales`, em milhões de cópias) no dataset **Video Game Sales** (*Kaggle*).

O projeto compara três abordagens sobre a mesma divisão Hold-out (80% treino / 20% teste):

- **Baseline (`DummyRegressor`):** prevê sempre a média do conjunto de treino, servindo de referência mínima.
- **MLP (alvo original):** `MLPRegressor` treinado diretamente sobre `Global_Sales`.
- **MLP (alvo em `log1p`):** `MLPRegressor` treinado sobre `log1p(Global_Sales)` para lidar com a forte assimetria da variável alvo, retornando à escala original com `expm1`.

## Modelagem

- **Variáveis preditoras (`X`):** `Platform`, `Genre`, `Year` e `Publisher_Clean` (Top 10 editoras mais frequentes + categoria `Other`), codificadas via *One-Hot Encoding* (`pd.get_dummies(..., drop_first=True)`).
- **Variável alvo (`y`):** `Global_Sales` (em milhões de cópias).
- **Prevenção de vazamento de dados (*data leakage*):** `Name` (identificador de alta cardinalidade) e as vendas regionais (`NA_Sales`, `EU_Sales`, `JP_Sales`, `Other_Sales`) são descartadas, pois `Global_Sales` é a soma direta das vendas regionais.
- **Limpeza:** remoção de registros com valores ausentes em `Year` ou `Publisher` (de 16.598 para 16.291 registros).
- **Padronização:** `StandardScaler` ajustado exclusivamente no conjunto de treino e aplicado no conjunto de teste.

## Parâmetros do Modelo

| Parâmetro | Valor |
|---|---|
| Algoritmo | `MLPRegressor` (scikit-learn) |
| Camadas ocultas | `(64, 32)` |
| Função de ativação | `relu` |
| Otimizador | `adam` |
| Máximo de iterações | `500` |
| Parada antecipada | `early_stopping=True` |
| Validação | Hold-out 80% treino / 20% teste |
| Padronização | `StandardScaler` |
| Semente aleatória | `random_state = 42` |

## Resultados

| Métrica | Baseline (média) | MLP (alvo original) | MLP (alvo em `log1p`) |
|---|:---:|:---:|:---:|
| MAE (milhões de cópias) | 0,6193 | 0,5679 | **0,4837** |
| MSE | 4,2791 | **3,9397** | 3,9952 |
| RMSE (milhões de cópias) | 2,0686 | **1,9849** | 1,9988 |
| MAPE (%) | 671,61% | 434,05% | **277,90%** |
| R² | -0,0003 | **0,0791** | 0,0661 |

## Visualizações geradas

Salva automaticamente na pasta `atividade_mlp/`:

| Arquivo | Conteúdo |
|---|---|
| `dispersao_real_vs_previsto.png` | Gráficos de dispersão Real vs. Previsto (escala log) com reta ideal ($y = x$) para a MLP no alvo original e em `log1p` |

## Pré-requisitos

- Python 3.10 ou superior
- pip

```bash
python --version
```

## Como executar

```bash
cd atividade_mlp
pip install -r requirements.txt
python mlp_videogames.py
```

Também é possível executar diretamente a partir da raiz do repositório:

```bash
python atividade_mlp/mlp_videogames.py
```

## Estrutura do projeto

```text
atividade_mlp/
│
├── mlp_videogames.py
├── vgsales.csv
├── dispersao_real_vs_previsto.png
├── README.md
└── requirements.txt
```
