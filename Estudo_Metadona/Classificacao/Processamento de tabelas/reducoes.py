import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# === Carregamento dos dados ===
df_reducoes = pd.read_csv("../Juncao e limpeza das tabelas processadas/reducoes.csv")  # substitui pelo caminho correto

# === Conversão de datas ===
df_reducoes["datareducao"] = pd.to_datetime(df_reducoes["datareducao"], errors='coerce')

# === Cálculo de estatísticas por utente ===
df_reducao_stats = df_reducoes.groupby("utente_id").agg(
    num_reducoes=("utente_id", "count"),
    media_dose_reducao=("doseareduzir", "mean"),
    media_periodo_reducao=("periodo", "mean"),
    data_primeira_reducao=("datareducao", "min"),
    data_ultima_reducao=("datareducao", "max")
).reset_index()

# === Cálculo do tempo entre a primeira e última redução ===
df_reducao_stats["tempo_reducoes_dias"] = (
    df_reducao_stats["data_ultima_reducao"] - df_reducao_stats["data_primeira_reducao"]
).dt.days

# (Opcional) Remover colunas de data se não forem necessárias
df_reducao_stats.drop(columns=["data_primeira_reducao", "data_ultima_reducao"], inplace=True)

# === Substituir NaNs por 0, se necessário para modelos ===
df_reducao_stats.fillna(0, inplace=True)

# === Ver resultado final ===
print(df_reducao_stats.tail())

# (Opcional) Guardar para análise/modelação
# df_reducao_stats.to_csv("estatisticas_reducoes_por_utente.csv", index=False)
