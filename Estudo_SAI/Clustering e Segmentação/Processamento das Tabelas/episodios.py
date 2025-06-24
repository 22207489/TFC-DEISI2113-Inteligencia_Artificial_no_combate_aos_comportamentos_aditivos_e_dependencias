import pandas as pd

# Carregar o ficheiro CSV com os episódios
df_episodios = pd.read_csv("episodios_202505181050.csv")

# Contar o número de episódios por utente
df_episodios_por_utente = df_episodios.groupby("utente_id").size().reset_index(name="total_episodios")

# Visualizar os primeiros resultados
print(df_episodios_por_utente.head())

# (Opcional) Guardar em ficheiro CSV
df_episodios_por_utente.to_csv("total_episodios_por_utente.csv", index=False)
