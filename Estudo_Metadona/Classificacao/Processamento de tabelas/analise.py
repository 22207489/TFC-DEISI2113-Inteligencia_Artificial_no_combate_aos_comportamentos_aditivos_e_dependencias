import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Carregar o ficheiro CSV
df = pd.read_csv("analises_feitas.csv")  # substitui pelo teu caminho

# Passo 1: Contar número total de testes por utente
testes_por_utente = df.groupby("utente_id").size().reset_index(name="num_testes")

# Passo 2: Dicionário com os nomes das análises
analises = {
    1: "VIH",
    2: "AGHBS",
    3: "ACHBS",
    4: "ACHBC",
    5: "ACHCV",
    6: "VDRL",
    7: "TPHA",
    8: "RX",
    9: "BK"
}

# Inicializar o DataFrame final com a contagem de testes
df_final = testes_por_utente.copy()

# Passo 3: Adicionar colunas com número total de análises por tipo
analises_por_tipo = df.groupby(["utente_id", "analise"]).size().unstack(fill_value=0)
analises_por_tipo.columns = [f"n_analises_{analises.get(col, col)}" for col in analises_por_tipo.columns]
df_final = df_final.merge(analises_por_tipo, on="utente_id", how="left")

# Passo 4: Criar colunas binárias indicando se teve pelo menos um resultado 'p' por tipo
for codigo, nome in analises.items():
    filtro = df[(df["analise"] == codigo) & (df["resultado"] == "p")]
    positivos = filtro.groupby("utente_id").size().reset_index(name=f"{nome}_positivo")
    positivos[f"{nome}_positivo"] = 1
    df_final = df_final.merge(positivos[["utente_id", f"{nome}_positivo"]], on="utente_id", how="left")

# Passo 5: Preencher NaN com 0 e converter para inteiro
df_final.fillna(0, inplace=True)
df_final = df_final.astype({col: int for col in df_final.columns if col != "utente_id"})

# Ver resultado
print(df_final.head())

# Guardar em CSV
df_final.to_csv("analises.csv", index=False)
