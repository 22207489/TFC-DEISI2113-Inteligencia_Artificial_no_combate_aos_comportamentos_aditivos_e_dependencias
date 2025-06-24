import pandas as pd

# Carregar as duas tabelas
df_1 = pd.read_csv("utentes.csv")       # Substitui pelo caminho correto
df_2 = pd.read_csv("subscritos.csv")        # Substitui pelo caminho correto

# Filtrar utentes da segunda tabela que estão no programa 1
ids_ute_programa_1 = df_2[df_2["programas"] == 1]["utente_id"].unique()

# Filtrar a primeira tabela com base nos utentes do programa 1
df_filtrado = df_1[df_1["utente_id"].isin(ids_ute_programa_1)]

# (Opcional) Guardar o resultado para CSV
df_filtrado.to_csv("utentes_metadona.csv", index=False)

# Ver as primeiras linhas
print(df_filtrado.head())
