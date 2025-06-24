import pandas as pd

# Carregar o ficheiro com os dados de ensinos
df_ensinos = pd.read_csv("ensino_endovenoso_202505181050.csv")  # Substitui pelo nome real do ficheiro se necessário

# Contar a quantidade de ensinos por utente
df_contagem_ensinos = df_ensinos.groupby("utente_id").size().reset_index(name="Total_Ensinos")

# Ver os primeiros resultados
print(df_contagem_ensinos.head())

# (Opcional) Guardar em CSV
df_contagem_ensinos.to_csv("total_ensinos_por_utente.csv", index=False)
