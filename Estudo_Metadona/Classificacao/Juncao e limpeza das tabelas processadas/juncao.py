import pandas as pd

# Lista de ficheiros
files = [
    "utentes_metadona.csv",
    "abandono.csv",
    "analises.csv",
    "estado_civilutentes.csv",
    "faltas.csv",
    "medicacao.csv",
    "reducoes.csv",
    "testes_rapidos.csv",
    "tomas_metadona.csv"
]

# Ficheiros com nomes de coluna do utente diferentes
colunas_personalizadas = {
    "estado_civilutentes.csv": "utente",
    "faltas.csv": "utente",
    "tomas_metadona.csv": "id_utente"
}

# Carregar tabela principal
df_merged = pd.read_csv("utentes_metadona.csv")

# Juntar os restantes ficheiros (apenas se tiverem IDs que existem em utentes_metadona)
for file in files[1:]:
    df_temp = pd.read_csv(file)
    # Renomear coluna de ID se necessário
    if file in colunas_personalizadas:
        df_temp.rename(columns={colunas_personalizadas[file]: "utente_id"}, inplace=True)
    # Fazer o left join com base apenas nos utentes da tabela principal
    df_merged = pd.merge(df_merged, df_temp, on="utente_id", how="left")

# Guardar resultado final (opcional)
df_merged.to_csv("tabela_unificada_base_metadona.csv", index=False)

# Mostrar primeiras linhas
print(df_merged.head())
