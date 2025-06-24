import pandas as pd

# Carregar o ficheiro CSV com os episódios psicossociais
df_psicossocial = pd.read_csv("psicossocial_episodio_202505181053.csv")

# Contar o número de episódios psicossociais por utente
df_episodios_psicossociais = df_psicossocial.groupby("utente_id").size().reset_index(name="total_episodios_psicossociais")

# Visualizar os primeiros resultados
print(df_episodios_psicossociais.head())

# (Opcional) Guardar o resultado num novo ficheiro CSV
df_episodios_psicossociais.to_csv("episodios_psicossociais_por_utente.csv", index=False)
