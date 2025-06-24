import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# Carregar o ficheiro com os materiais usados
df_materiais = pd.read_csv("materiais_episodio_202505181051.csv")

# Criar tabela com a quantidade de cada material usado por utente
df_materiais_pivot = df_materiais.pivot_table(
    index="utente_id",
    columns="material",
    values="qtd",
    aggfunc="sum",
    fill_value=0
)

# Dicionário com os nomes legíveis dos materiais
nomes_materiais = {
    1: "KITS_IV",
    2: "SERINGA_23G",
    3: "SERINGA_25G",
    4: "SERINGA_26G",
    5: "AGUA",
    6: "FILTRO",
    7: "TOALHETE",
    8: "CACHIMBO_1",
    9: "CACHIMBO_2",
    10: "PRATA",
    11: "RECIPIENTE",
    12: "DEVOLUCAO_MATERIAL",
    13: "PRESERVATIVO_EXTERNO",
    14: "PRESERVATIVO_INTERNO",
    29: "SERINGA_29G"
}

# Renomear colunas com os nomes dos materiais
df_materiais_pivot.rename(columns=nomes_materiais, inplace=True)

# Resetar índice para manter utente_id como coluna normal
df_materiais_pivot.reset_index(inplace=True)

# Visualizar resultado
print(df_materiais_pivot.head())

# (Opcional) Guardar em CSV
df_materiais_pivot.to_csv("materiais_usados_por_utente.csv", index=False)
