import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# Carregar o ficheiro com os dados de administração de medicamentos
df_meds = pd.read_csv("tomas_medicacao_202505181055.csv")

# Criar tabela com contagem de medicamentos tomados por utente
df_meds_pivot = df_meds.pivot_table(
    index="utente_id",
    columns="medicamento_id",
    values="id",
    aggfunc="count",
    fill_value=0
)

# Renomear colunas com os nomes legíveis dos medicamentos
medicamentos_map = {
    1: "Medicacao_Antibacilar",
    2: "Medicacao_ARV_VIH",
    3: "Medicacao_VHC",
    4: "Medicacao_Psiquiatrica",
    5: "Outra"
}

df_meds_pivot.rename(columns=medicamentos_map, inplace=True)

# Resetar o índice para manter utente_id como coluna
df_meds_pivot.reset_index(inplace=True)

# Visualizar os primeiros resultados
print(df_meds_pivot.head())

# (Opcional) Guardar em CSV
df_meds_pivot.to_csv("medicamentos_por_utente.csv", index=False)
