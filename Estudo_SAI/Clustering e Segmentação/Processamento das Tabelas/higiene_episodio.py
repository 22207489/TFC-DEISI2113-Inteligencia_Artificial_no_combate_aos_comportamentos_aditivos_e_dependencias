import pandas as pd

# Carregar o ficheiro de produtos de higiene por episódio
df_higiene = pd.read_csv("higiene_episodio_202505181051.csv")  # substitui pelo nome correto do ficheiro CSV

# Dicionário com nomes legíveis dos produtos
produtos_higiene = {
    1: "CHINELO", 2: "TOALHA", 3: "GEL_BANHO", 4: "SHAMPOO", 5: "AMACIADOR",
    6: "PENSOS_HIGIENICOS", 7: "TAMPOES", 8: "LAMINAS_BARBEAR", 9: "ESCOVA_DENTES",
    10: "PASTA_DENTES", 11: "DESODORIZANTE", 12: "TOALHITAS", 13: "OUTRO"
}

# Agrupar e somar quantidade de produtos por episódio e tipo de produto
df_higiene_agg = df_higiene.groupby(['episodio', 'higiene'])['qtd'].sum().unstack(fill_value=0)

# Substituir os códigos dos produtos pelos nomes
df_higiene_agg.rename(columns=produtos_higiene, inplace=True)

# Resetar o índice para transformar 'episodio' em coluna normal
df_higiene_agg.reset_index(inplace=True)

# Mostrar os primeiros resultados
print(df_higiene_agg.head())

# (Opcional) Guardar em ficheiro CSV
#df_higiene_agg.to_csv("produtos_higiene_por_episodio.csv", index=False)
