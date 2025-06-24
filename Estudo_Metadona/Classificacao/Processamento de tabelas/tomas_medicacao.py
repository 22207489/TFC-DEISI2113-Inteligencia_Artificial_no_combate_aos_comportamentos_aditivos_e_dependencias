import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# Carregar o ficheiro CSV
df = pd.read_csv("tomas_medicacao.csv")

# Criar coluna com quantidade total de medicamentos administrados por utente
df['total_tomas_medicacao'] = df.groupby('utente_id')['medicamento_id'].transform('count')

# Mapear IDs de medicamentos para nomes legíveis
medicamentos_map = {
    1: 'medicamento_Antibacilar',
    2: 'medicamento_ARV_VIH',
    3: 'medicamento_VHC',
    4: 'medicamento_Psiquiatrica',
    5: 'Outra'
}

# Criar colunas binárias por tipo de medicamento
for med_id, med_name in medicamentos_map.items():
    df[med_name] = df['medicamento_id'].apply(lambda x: 1 if x == med_id else 0)

# Agrupar por utente_id para obter os resultados finais
df_resultado = df.groupby('utente_id').agg({
    'total_tomas_medicacao': 'first',
    'medicamento_Antibacilar': 'max',
    'medicamento_ARV_VIH': 'max',
    'medicamento_VHC': 'max',
    'medicamento_Psiquiatrica': 'max',
    'Outra': 'max'
}).reset_index()
df_resultado.to_csv("medicacao.csv", index=False)

# Visualizar o resultado
print(df_resultado.head())
