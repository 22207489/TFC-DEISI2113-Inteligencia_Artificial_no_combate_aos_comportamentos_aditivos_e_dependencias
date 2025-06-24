import pandas as pd

# Carregar o ficheiro CSV com os dados
df = pd.read_csv("apoio_endovenoso_202505181048.csv")

# Filtrar apenas os apoios de injeção do tipo 1 e 2
df_filtrado = df[df["apoioinjecao"].isin([1, 2])]

# Criar uma tabela com a contagem por tipo de apoio e por utente
df_resultado = df_filtrado.pivot_table(
    index="utente_id",
    columns="apoioinjecao",
    values="id",
    aggfunc="count",
    fill_value=0
).reset_index()

# Renomear colunas para nomes mais compreensíveis
df_resultado.columns.name = None
df_resultado.rename(columns={1: "Canalizar_acesso", 2: "Tentativas"}, inplace=True)

# Adicionar coluna com o total de apoios endovenosos
df_resultado["Total_Apoios_Endovenosos"] = (
    df_resultado["Canalizar_acesso"] + df_resultado["Tentativas"]
)

# Ver os primeiros resultados
print(df_resultado.head())

# (Opcional) Guardar em ficheiro CSV
df_resultado.to_csv("apoio_injecao_por_utente.csv", index=False)
