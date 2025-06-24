import pandas as pd
from datetime import datetime

# === Carregar os dados ===
df_programa = pd.read_csv("programa_202505181101.csv")

# === Preparar datas ===
df_programa["entrada"] = pd.to_datetime(df_programa["entrada"], errors='coerce')
df_programa["saida"] = pd.to_datetime(df_programa["saida"], errors='coerce')
data_atual = pd.to_datetime("2024-01-01")  # ou datetime.today()

# === Variáveis derivadas ===
df_programa["tempo_total_dias_no_programa"] = (
    df_programa["saida"].fillna(data_atual) - df_programa["entrada"]
).dt.days

df_programa["num_admissoes"] = df_programa.groupby("utente_id")["id"].transform("count")
df_programa["num_saidas"] = df_programa.groupby("utente_id")["saida"].transform(lambda x: x.notna().sum())
df_programa["ativo_atualmente"] = df_programa["saida"].isna().astype(int)

# === Marcar última estadia por utente ===
df_programa.sort_values(["utente_id", "entrada"], inplace=True)
df_programa["is_ultima_estadia"] = (
    df_programa.groupby("utente_id")["entrada"].transform("max") == df_programa["entrada"]
)

# === Criar coluna binária de saída sem retorno ===
df_programa["saida_sem_retorno_binario"] = df_programa.apply(
    lambda row: 1 if (row["is_ultima_estadia"] and row["motivo_id"] > 0 and pd.notna(row["saida"])) else 0,
    axis=1
)

# === Agregar saída sem retorno binária por utente ===
df_saida_binaria = df_programa.groupby("utente_id")["saida_sem_retorno_binario"].max().reset_index()

# === Agregar dados principais por utente ===
df_utentes_agg = df_programa.groupby("utente_id").agg({
    "num_admissoes": "max",
    "num_saidas": "max",
    "ativo_atualmente": "max"
}).reset_index()

# === Juntar com coluna binária de saída ===
df_final = df_utentes_agg.merge(df_saida_binaria, on="utente_id", how="left")

# === Guardar ou visualizar ===
df_final.to_csv("abandono.csv", index=False)
print(df_final.head())
