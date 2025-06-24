import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# Carregar o ficheiro CSV com os dados de consumo por fumo
df_fumo = pd.read_csv("substancias_fumado_202505181054.csv")

# Criar tabela com contagem de cada substância fumada por utente
df_fumo_pivot = df_fumo.pivot_table(
    index="utente_id",
    columns="substancia",
    values="id",
    aggfunc="count",
    fill_value=0
)

# Dicionário com nomes legíveis das substâncias
substancias_map = {
    1: "HEROINA_FUMADA",
    2: "COCAINA_FUMADA",
    3: "HEROINA_COCAINA_FUMADAS",
    4: "BZD_FUMADA",
    5: "METADONA_FUMADA",
    6: "METANFETAMINAS_FUMADA",
    7: "OUTRO_FUMADA"
}

# Renomear colunas
df_fumo_pivot.rename(columns=substancias_map, inplace=True)

# Resetar índice para manter utente_id como coluna normal
df_fumo_pivot.reset_index(inplace=True)

# Visualizar os primeiros resultados
print(df_fumo_pivot.head())

# (Opcional) Guardar em ficheiro CSV
df_fumo_pivot.to_csv("consumo_fumado_por_substancia.csv", index=False)
