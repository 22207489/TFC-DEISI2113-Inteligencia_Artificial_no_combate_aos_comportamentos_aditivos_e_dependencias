import pandas as pd

# Carregar os ficheiros CSV
df_programas = pd.read_csv("subscritos_202505181054.csv")  # Ex: programas.csv
df_segunda = pd.read_csv("utentes_202505181055.csv")      # Ex: info_utentes.csv

# Filtrar apenas os utentes que pertencem ao programa 2
utentes_programa_2 = df_programas[df_programas["programas"] == 2]["utente_id"].unique()

# Filtrar a segunda tabela para manter apenas esses utentes
df_filtrado = df_segunda[df_segunda["utente_id"].isin(utentes_programa_2)]

# Ver resultado
print(df_filtrado.head())

# (Opcional) Guardar em CSV
df_filtrado.to_csv("utentes_SAI.csv", index=False)
