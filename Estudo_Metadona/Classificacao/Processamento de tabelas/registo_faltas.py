import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# === 1. Carregar os dados ===
df = pd.read_csv("registo_faltas.csv")  # Substitui pelo caminho correto se necessário

# === 2. Preparar timestamp e filtrar apenas data ===
df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
df["data_ocorrencia"] = df["timestamp"].dt.date  # Ignora horas, minutos e segundos

# === 3. Agrupar por utente e data para identificar ocorrência real ===
df_ocorrencias = df.groupby(["utente", "data_ocorrencia"]).agg(
    faltas=("faltas", "first"),
    valor_a_recuperar=("valor_a_recuperar", "first"),
    total_tomas_recuperacao=("total_tomas_recuperacao", "first"),
    tomas_efetuadas=("tomada", lambda x: x.sum())  # Conta os True
).reset_index()

# === 4. Calcular se recuperou e quantas falhou ===
df_ocorrencias["recuperou"] = (df_ocorrencias["total_tomas_recuperacao"] == df_ocorrencias["tomas_efetuadas"]).astype(int)

# === 5. Numerar as ocorrências por utente ===
df_ocorrencias["numero_ocorrencia"] = df_ocorrencias.groupby("utente").cumcount() + 1

# === 6. Reorganizar colunas ===
df_final = df_ocorrencias[[
    "utente", "numero_ocorrencia", "faltas", "valor_a_recuperar",
    "total_tomas_recuperacao", "tomas_efetuadas",  "recuperou"
]]

# === 7. (Opcional) Guardar para CSV ===
df_final.to_csv("faltas.csv", index=False)

# Ver resultado
print(df_final.head())
