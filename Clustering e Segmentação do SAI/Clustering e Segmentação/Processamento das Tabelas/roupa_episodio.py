import pandas as pd

# Carregar o ficheiro CSV com os dados das roupas usadas por episódio
df_roupa = pd.read_csv("roupa_episodio_202505181054.csv")  # Substitui pelo nome real do ficheiro

# Dicionário com os nomes legíveis das peças de roupa
pecas_roupa = {
    1: "CUECA",
    2: "MEIA",
    3: "CASACO",
    4: "CALCAS",
    5: "CAMISOLA",
    6: "SAIA_VESTIDO",
    7: "CALCADO",
    8: "OUTRO"
}

# Agrupar por episódio e tipo de roupa, somando as quantidades
df_roupa_agg = df_roupa.groupby(['episodio', 'roupa'])['qtd'].sum().unstack(fill_value=0)

# Renomear as colunas de acordo com os nomes legíveis
df_roupa_agg.rename(columns=pecas_roupa, inplace=True)

# Resetar o índice para tornar 'episodio' uma coluna visível
df_roupa_agg.reset_index(inplace=True)

# Mostrar os primeiros resultados
print(df_roupa_agg.head())

# (Opcional) Guardar em ficheiro CSV
df_roupa_agg.to_csv("roupa_por_episodio.csv", index=False)
