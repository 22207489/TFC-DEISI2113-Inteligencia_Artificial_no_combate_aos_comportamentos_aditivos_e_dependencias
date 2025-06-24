import pandas as pd

# Mostrar todas as colunas e linhas no output
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Carregar o ficheiro CSV com os dados de testes
df_testes = pd.read_csv("testes_rapidos_utentes_202505181054.csv")

# Mapas para nomes legíveis
tipos_teste = {
    1: "TESTES_VIH",
    2: "TESTES_AGHBS",
    3: "TESTES_VHC",
    4: "TESTES_Sifilis",
    5: "TESTES_RnaHCV"
}

resultados_map = {
    1: "Reativo",
    2: "NaoReativo",
    3: "Inconclusivo"
}

# Substituir os códigos pelos nomes
df_testes["teste_nome"] = df_testes["teste"].map(tipos_teste)
df_testes["resultado_nome"] = df_testes["resultado"].map(resultados_map)

# Contagem total de testes por utente e tipo de teste
df_total_testes = df_testes.pivot_table(
    index="utente_id",
    columns="teste_nome",
    values="id",
    aggfunc="count",
    fill_value=0
)

# Contagem de testes reativos por utente e tipo de teste
df_reativos = df_testes[df_testes["resultado_nome"] == "Reativo"].pivot_table(
    index="utente_id",
    columns="teste_nome",
    values="id",
    aggfunc="count",
    fill_value=0
)

# Renomear colunas dos reativos
df_reativos.columns = [f"RESULTADOS_{col}_POSITIVOS" for col in df_reativos.columns]

# Juntar as duas tabelas
df_testes_completo = df_total_testes.merge(df_reativos, on="utente_id", how="left").fillna(0).astype(int)

# Adicionar coluna com o total de testes realizados por utente
df_testes_completo["TOTAL_TESTES_REALIZADOS"] = df_total_testes.sum(axis=1)

# Ver os primeiros resultados
print(df_testes_completo.head())

# (Opcional) Guardar para CSV
df_testes_completo.to_csv("testes_resultados_por_utente.csv", index=True)
