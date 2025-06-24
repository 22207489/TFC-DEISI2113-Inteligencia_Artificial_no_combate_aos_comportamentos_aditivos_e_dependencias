import pandas as pd
from datetime import datetime

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# === Carregar os dados ===
df_programa = pd.read_csv("programa.csv")

# === Preparar datas ===
df_programa["entrada"] = pd.to_datetime(df_programa["entrada"], errors='coerce')
df_programa["saida"] = pd.to_datetime(df_programa["saida"], errors='coerce')

# Data de corte para utentes ainda ativos (último dia de maio de 2025)
data_corte = pd.to_datetime("2025-05-31")

# === Variáveis derivadas já existentes ===
df_programa["tempo_total_dias_no_programa"] = (
    df_programa["saida"].fillna(data_corte) - df_programa["entrada"]
).dt.days.round().astype(int)

df_programa["num_admissoes"] = df_programa.groupby("utente_id")["id"].transform("count")
df_programa["num_saidas"] = df_programa.groupby("utente_id")["saida"].transform(lambda x: x.notna().sum())
df_programa["ativo_atualmente"] = df_programa["saida"].isna().astype(int)

df_programa.sort_values(["utente_id", "entrada"], inplace=True)
df_programa["is_ultima_estadia"] = (
    df_programa.groupby("utente_id")["entrada"].transform("max") == df_programa["entrada"]
)

df_programa["saida_sem_retorno_abandono"] = df_programa.apply(
    lambda row: 1 if (row["is_ultima_estadia"] and row["motivo_id"] == 20 and pd.notna(row["saida"])) else 0,
    axis=1
)

df_programa["saida_sem_retorno_motivo"] = df_programa.apply(
    lambda row: row["motivo_id"] if (row["is_ultima_estadia"] and pd.notna(row["saida"])) else 0,
    axis=1
)

def ajustar_codigos_saida(df):
    mapeamento_codigos = {
        20: 1, 21: 2, 22: 3, 23: 4, 24: 5, 25: 6,
        26: 7, 27: 8, 28: 9, 29: 10, 30: 11,
        31: 12, 32: 13
    }
    df["saida_sem_retorno_motivo"] = df["saida_sem_retorno_motivo"].map(mapeamento_codigos)
    return df

df_programa = ajustar_codigos_saida(df_programa)

# === Calcular tempo médio de estadia por utente ===
media_estadia = df_programa.groupby("utente_id")["tempo_total_dias_no_programa"].mean().round().astype(int)
df_media = media_estadia.reset_index().rename(columns={"tempo_total_dias_no_programa": "tempo_medio_estadia"})

# === Agregar saída sem retorno binária por utente ===
df_saida_binaria = df_programa.groupby("utente_id")["saida_sem_retorno_abandono"].max().reset_index()
df_saida = df_programa.groupby("utente_id")["saida_sem_retorno_motivo"].max().reset_index()

# === Agregar dados principais por utente ===
df_utentes_agg = df_programa.groupby("utente_id").agg({
    "num_admissoes": "max",
    "num_saidas": "max",
    "ativo_atualmente": "max"
}).reset_index()

# === Juntar com coluna binária de saída ===
df_final = df_utentes_agg.merge(df_saida_binaria, on="utente_id", how="left")
df_final_merged = df_final.merge(df_saida, on="utente_id", how="left")

# === Acrescentar tempo médio de estadia ===
df_final_merged = df_final_merged.merge(df_media, on="utente_id", how="left")

# === Guardar ou visualizar ===
df_final_merged.to_csv("abandono.csv", index=False)
print(df_final_merged.head())
