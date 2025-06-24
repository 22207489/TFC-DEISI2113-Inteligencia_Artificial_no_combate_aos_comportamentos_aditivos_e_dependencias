import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# === Carregar tabelas mais recentes ===

# === Carregar tabelas memorizadas ===
df1 = pd.read_csv("analises_completas_por_utente.csv")
df2 = pd.read_csv("apoio_injecao_por_utente.csv")
df3 = pd.read_csv("atos_enfermagem_por_utente.csv")
df4 = pd.read_csv("avaliacoes_por_utente.csv")
df5 = pd.read_csv("consumo_fumado_por_substancia.csv")
df6 = pd.read_csv("consumo_substancias_locais_filtrado.csv")
df7 = pd.read_csv("episodios_psicossociais_por_utente.csv")
df8 = pd.read_csv("materiais_usados_por_utente.csv")
df9 = pd.read_csv("medicamentos_por_utente.csv")
df10 = pd.read_csv("abandono.csv")
df11 = pd.read_csv("testes_resultados_por_utente.csv")
df12 = pd.read_csv("total_actos_por_utente.csv")
df13 = pd.read_csv("total_ensinos_por_utente.csv")
df14 = pd.read_csv("total_episodios_por_utente.csv")

# === Fazer merge progressivo com base em utente_id ===
df_final = df1.copy()
for df in [df2, df3, df4, df5, df6, df7, df8, df9, df10,df11,df12,df13,df14]:
    if "utente_id" in df.columns:
        df_final = df_final.merge(df, on="utente_id", how="outer")

df.rename(columns={'ACHBC': 'ANALISES_ACHBC'}, inplace=True)
df.rename(columns={'ACHBS': 'ANALISES_ACHBS'}, inplace=True)
df.rename(columns={'ACHCV': 'ANALISES_ACHCV'}, inplace=True)
df.rename(columns={'AGHBS': 'ANALISES_AGHBS'}, inplace=True)
df.rename(columns={'BK': 'ANALISES_BK'}, inplace=True)
df.rename(columns={'RX': 'ANALISES_RX'}, inplace=True)
df.rename(columns={'TPHA': 'ANALISES_TPHA'}, inplace=True)
df.rename(columns={'VDRL': 'ANALISES_VDRL'}, inplace=True)
df.rename(columns={'VIH': 'ANALISES_VIH'}, inplace=True)


# === Exportar resultado final (opcional) ===
df_final.to_csv("dataset_final_utentes.csv", index=False)

# === Pré-visualizar os primeiros dados ===
print(df_final.head())
