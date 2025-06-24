import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# Carregar o ficheiro com os dados de consumo
df_consumo = pd.read_csv("substancias_endovenoso_202505181054.csv")

# Substituir valores nulos por 0 e garantir tipo inteiro
df_consumo["substancia"] = df_consumo["substancia"].fillna(0).astype(int)
df_consumo["local"] = df_consumo["local"].fillna(0).astype(int)

# Criar tabela com contagem de substâncias por utente
df_substancias = df_consumo.pivot_table(
    index="utente_id",
    columns="substancia",
    values="id",
    aggfunc="count",
    fill_value=0
)

# Criar tabela com contagem de locais por utente
df_locais = df_consumo.pivot_table(
    index="utente_id",
    columns="local",
    values="id",
    aggfunc="count",
    fill_value=0
)

# Remover substâncias desnecessárias (4, 5, 6) e locais desnecessários (4, 6, 7)
df_substancias = df_substancias.drop(columns=[4, 5, 6], errors='ignore')
df_locais = df_locais.drop(columns=[4, 6, 7], errors='ignore')

# Renomear colunas
df_substancias.rename(columns={
    1: "HEROINA_INJETADA",
    2: "COCAINA_INJETADA",
    3: "HEROINA_COCAINA_INJETADAS",
    7: "OUTRA_SUBSTANCIA_INJETADA"
}, inplace=True)

df_locais.rename(columns={
    0: "sem_local_injecao",
    1: "Pe",
    2: "Perna",
    3: "Inguinal",
    5: "Braco_Antebraco"
}, inplace=True)

# Juntar as duas tabelas
df_consumo_final = df_substancias.merge(df_locais, on="utente_id", how="outer").fillna(0)

# Converter todos os valores para inteiros
df_consumo_final = df_consumo_final.astype(int)

# Visualizar os primeiros resultados
print(df_consumo_final.head())

# (Opcional) Guardar em CSV
df_consumo_final.to_csv("consumo_substancias_locais_filtrado.csv", index=True)
