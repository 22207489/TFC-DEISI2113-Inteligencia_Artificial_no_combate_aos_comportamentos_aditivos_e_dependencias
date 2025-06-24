import pandas as pd

# Carregar o ficheiro com os dados originais
df = pd.read_csv("actosenfermagemconsumo.csv")

# Converter a coluna de timestamp para datetime (opcional, útil se quiseres futuramente fazer análises por data)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Agrupar por utente_id e contar o número total de atos
df_actos_totais = df.groupby("utente_id").agg(
    total_actos=("acto", "count")
).reset_index()

# Visualizar os primeiros resultados
print(df_actos_totais.head())

# (Opcional) Guardar em ficheiro CSV
df_actos_totais.to_csv("total_actos_por_utente.csv", index=False)
