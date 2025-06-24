import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# Carregar os dados do CSV
df_analises = pd.read_csv("analises_feitas_202505181047.csv")

# Dicionário completo com nomes legíveis
analises_map_completo = {
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

# Mapear nomes das análises
df_analises["analise_nome"] = df_analises["analise"].map(analises_map_completo)

# Contagem total de análises por tipo e utente
df_total_analises = df_analises.pivot_table(
    index="utente_id",
    columns="analise_nome",
    values="id",
    aggfunc="count",
    fill_value=0
)

# Contagem de análises com resultado positivo
df_positivas = df_analises[df_analises["resultado"] == "p"].pivot_table(
    index="utente_id",
    columns="analise_nome",
    values="id",
    aggfunc="count",
    fill_value=0
)

# Renomear colunas para indicar positivo
df_positivas.columns = [f"{col}_Positivo" for col in df_positivas.columns]

# Juntar totais com positivos
df_analises_final = df_total_analises.merge(df_positivas, on="utente_id", how="left").fillna(0).astype(int)

# Adicionar coluna com total de análises realizadas por utente
df_analises_final["Total_Analises"] = df_total_analises.sum(axis=1)

# Ver resultado
print(df_analises_final.head())

# (Opcional) Guardar em ficheiro CSV
df_analises_final.to_csv("analises_completas_por_utente.csv", index=True)
