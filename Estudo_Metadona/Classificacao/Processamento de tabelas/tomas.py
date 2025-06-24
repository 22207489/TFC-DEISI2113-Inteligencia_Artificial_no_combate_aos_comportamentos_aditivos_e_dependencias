import pandas as pd

# Carregar o ficheiro
df = pd.read_csv("tomas_202505181102.csv", low_memory=False)

# Converter datas
df["data"] = pd.to_datetime(df["data"], errors='coerce')

# Ordenar
df = df.sort_values(by=["id_utente", "data"])

# Flags para toma e falta
df["toma_flag"] = (df["id_status"] == "t")
df["falta_flag"] = (df["id_status"] == "f")

# Total por utente
df_agg = df.groupby("id_utente").agg({
    "toma_flag": "sum",
    "falta_flag": "sum"
}).reset_index().rename(columns={
    "toma_flag": "n_dias_com_toma",
    "falta_flag": "n_dias_com_falta"
})

# Função para dias consecutivos sem toma
def max_consecutivos_sem_toma(subdf):
    subdf = subdf.sort_values("data")
    subdf["falta"] = (subdf["id_status"] == "f").astype(int)
    subdf["grupo"] = (subdf["falta"] != subdf["falta"].shift()).cumsum()
    grupos = subdf[subdf["falta"] == 1].groupby("grupo").size()
    return grupos.max() if not grupos.empty else 0

# Aplicar por utente
df_consecutivos = df.groupby("id_utente").apply(max_consecutivos_sem_toma).reset_index(name="max_dias_consecutivos_sem_toma")

# Juntar tudo
df_resultado = df_agg.merge(df_consecutivos, on="id_utente", how="left")

# Guardar em CSV se quiseres
df_resultado.to_csv("tomas_metadona.csv", index=False)
