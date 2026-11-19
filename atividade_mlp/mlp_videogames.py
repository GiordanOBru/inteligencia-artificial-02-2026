"""
Regressao com Rede Neural MLP - Video Game Sales
Alvo: Global_Sales (milhoes de copias)
Validacao: Hold-out 80/20
"""
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.dummy import DummyRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
    r2_score,
)

warnings.filterwarnings("ignore", category=UserWarning)

BASE_DIR = Path(__file__).resolve().parent

# Carregamento
dados = pd.read_csv(BASE_DIR / "vgsales.csv")
print(f"Registros originais: {len(dados)}")

# Limpeza de nulos
dados = dados.dropna(subset=["Year", "Publisher"])
print(f"Registros apos dropna: {len(dados)}")

# Top 10 editores + 'other
top_editores = dados["Publisher"].value_counts().nlargest(10).index
dados["Publisher_Clean"] = dados["Publisher"].apply(
    lambda x: x if x in top_editores else "Other"
)

# Features e alvo
features = ["Platform", "Genre", "Year", "Publisher_Clean"]
X = pd.get_dummies(dados[features], drop_first=True).astype(float)
y = dados["Global_Sales"]

# Hold-out 80/20 
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# Padronizacao 
scaler = StandardScaler()
X_treino_s = scaler.fit_transform(X_treino)
X_teste_s = scaler.transform(X_teste)

# Alvo em escala log 
y_treino_log = np.log1p(y_treino)


def avaliar(nome, y_real, y_prev):
    mae = mean_absolute_error(y_real, y_prev)
    mse = mean_squared_error(y_real, y_prev)
    rmse = np.sqrt(mse)
    mape = mean_absolute_percentage_error(y_real, y_prev) * 100
    r2 = r2_score(y_real, y_prev)
    print(f"\n=== {nome} ===")
    print(f"MAE  (Erro Medio Absoluto):            {mae:.4f} milhoes de copias")
    print(f"MSE  (Erro Quadratico Medio):          {mse:.4f}")
    print(f"RMSE (Raiz do Erro Quadratico Medio):  {rmse:.4f} milhoes de copias")
    print(f"MAPE (Erro Percentual Medio):          {mape:.2f}%")
    print(f"R2   (Coeficiente de Determinacao):    {r2:.4f}")
    return dict(MAE=mae, MSE=mse, RMSE=rmse, MAPE=mape, R2=r2)


# Baseline: prever sempre a media do treino
dummy = DummyRegressor(strategy="mean").fit(X_treino_s, y_treino)
res_base = avaliar("BASELINE (media)", y_teste, dummy.predict(X_teste_s))

# MLP conforme o planejamento (alvo original)
mlp = MLPRegressor(
    hidden_layer_sizes=(64, 32),
    activation="relu",
    solver="adam",
    max_iter=500,
    early_stopping=True,
    random_state=42,
)
mlp.fit(X_treino_s, y_treino)
res_mlp = avaliar("MLP (alvo original)", y_teste, mlp.predict(X_teste_s))

# MLP com alvo em log (volta a escala original com expm1)
mlp_log = MLPRegressor(
    hidden_layer_sizes=(64, 32),
    activation="relu",
    solver="adam",
    max_iter=500,
    early_stopping=True,
    random_state=42,
)
mlp_log.fit(X_treino_s, y_treino_log)
y_pred_log = np.clip(np.expm1(mlp_log.predict(X_teste_s)), 0, None)
res_log = avaliar("MLP (alvo em log1p)", y_teste, y_pred_log)

# Tabela comparativa
print("\n=== COMPARATIVO ===")
print(pd.DataFrame(
    {"Baseline": res_base, "MLP": res_mlp, "MLP log": res_log}
).round(4).to_string())

# Graficos de dispersao Real vs Previsto
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
for ax, pred, titulo in zip(
    axes,
    [mlp.predict(X_teste_s), y_pred_log],
    ["MLP (alvo original)", "MLP (alvo em log1p)"],
):
    pred = np.clip(pred, 0.005, None)
    ax.scatter(y_teste, pred, alpha=0.3, color="steelblue", label="Observacoes")
    lim = [0.005, max(y_teste.max(), pred.max())]
    ax.plot(lim, lim, "r--", label="Predicao ideal (y = x)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(titulo)
    ax.set_xlabel("Vendas reais (milhoes de copias, escala log)")
    ax.set_ylabel("Vendas previstas (milhoes de copias, escala log)")
    ax.legend()
    ax.grid(True, alpha=0.3)
plt.suptitle("Vendas Globais de Jogos Eletronicos - Real vs. Previsto")
plt.tight_layout()
caminho_grafico = BASE_DIR / "dispersao_real_vs_previsto.png"
plt.savefig(caminho_grafico, dpi=150)
print(f"\nGrafico salvo em {caminho_grafico}")
