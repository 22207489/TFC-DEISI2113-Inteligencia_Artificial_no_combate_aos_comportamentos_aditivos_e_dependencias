import pandas as pd

# === Carregar os dados ===
df_testes = pd.read_csv("testes_rapidos_utentes.csv")  # substitui pelo caminho correto

# === Mapeamento dos nomes dos testes ===
mapa_testes = {
    1: 'VIH',
    2: 'AGHBS',
    3: 'VHC',
    4: 'Sifilis',
    5: 'RnaHCV'
}

df_testes['teste_nome'] = df_testes['teste'].map(mapa_testes)

# === Filtrar testes válidos (1 = reativo, 2 = não reativo) ===
df_validos = df_testes[df_testes['resultado'].isin([1, 2])].copy()

# === Criar coluna binária "reativo" ===
df_validos['reativo'] = (df_validos['resultado'] == 1).astype(int)

# === Total de testes válidos por utente ===
df_total = df_validos.groupby("utente_id").size().reset_index(name="total_testes_validos")

# === Total de testes reativos por utente ===
df_total_reativos = df_validos.groupby("utente_id")["reativo"].sum().reset_index(name="reativos_total")

# === Número de testes por tipo de teste (VIH, AGHBS, etc.) ===
df_testes_tipo = df_validos.groupby(["utente_id", "teste_nome"]).size().unstack(fill_value=0)
df_testes_tipo.columns = [f"n_testes_{col}" for col in df_testes_tipo.columns]

# === Flags binárias de reatividade por tipo ===
df_flags = df_validos[df_validos['reativo'] == 1].pivot_table(
    index='utente_id',
    columns='teste_nome',
    values='reativo',
    aggfunc='max'
).fillna(0).astype(int)
df_flags.columns = [f"{col}_reativo" for col in df_flags.columns]

# === Juntar tudo num único DataFrame final ===
df_resultado = df_total.merge(df_total_reativos, on="utente_id", how="left")
df_resultado = df_resultado.merge(df_testes_tipo, on="utente_id", how="left")
df_resultado = df_resultado.merge(df_flags, on="utente_id", how="left")
df_resultado.fillna(0, inplace=True)
df_resultado = df_resultado.astype({col: int for col in df_resultado.columns if col != 'utente_id'})

# === Guardar ou visualizar ===
df_resultado.to_csv("testes_rapidos.csv", index=False)
print(df_resultado.head())
