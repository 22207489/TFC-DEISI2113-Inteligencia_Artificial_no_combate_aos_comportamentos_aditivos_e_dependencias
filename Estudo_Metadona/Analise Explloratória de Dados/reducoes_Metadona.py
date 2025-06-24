import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Carregar os dados
df_utentes = pd.read_csv(r"C:/TFC/EstudoMetadona/dados/utentes/utentes.csv")
df_reducoes = pd.read_csv("reducoes.csv")

# Filtrar apenas utentes que participam no programa de metadona
df_participantes_reducoes = df_utentes[df_utentes['prog_metadona'] == True]

# Filtrar reduções apenas para utentes participantes
df_reducoes_participantes = df_reducoes[df_reducoes['utente_id'].isin(df_participantes_reducoes['utente_id'])]

# Corrigir colunas de datas
df_reducoes_participantes['data'] = pd.to_datetime(df_reducoes_participantes['data'], errors='coerce')
df_reducoes_participantes['datareducao'] = pd.to_datetime(df_reducoes_participantes['datareducao'], errors='coerce')
df_reducoes_participantes['data_ultima_reducao'] = pd.to_datetime(df_reducoes_participantes['data_ultima_reducao'], errors='coerce')

# --------------------------------------------------------------------------------------------------------------------
# 1. Distribuição das doses a reduzir
plt.figure(figsize=(10,6))
df_reducoes_participantes['doseareduzir'].dropna().astype(float).plot(kind='hist', bins=20, color='skyblue', edgecolor='black')
plt.title('Distribuição das Doses a Reduzir')
plt.xlabel('Dose a Reduzir (mg)')
plt.ylabel('Número de Utentes')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#---------------------------------------------------------------------------------------------------
# 5. Tempo planeado de redução
tempo_reducao = (df_reducoes_participantes['data_ultima_reducao'] - df_reducoes_participantes['datareducao']).dt.days.abs()
tempo_utente = (df_reducoes_participantes[df_reducoes_participantes['utente_id'] == 6544]['data_ultima_reducao']-df_reducoes_participantes[df_reducoes_participantes['utente_id'] == 6544]['datareducao']).dt.days.abs()

plt.figure(figsize=(10,6))
tempo_reducao.dropna().plot(kind='hist', bins=30, color='gold', edgecolor='black')
plt.title('Tempo Planeado de Redução (Dias)')
plt.xlabel('Dias Planeados para Redução')
plt.ylabel('Número de Utentes')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
print(tempo_utente)
# --------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------
# 10. Média de redução por ano
media_reducao_ano = df_reducoes_participantes.groupby(df_reducoes_participantes['data'].dt.year)['doseareduzir'].mean()

plt.figure(figsize=(10,6))
media_reducao_ano.plot(kind='bar', color='teal')
plt.title('Média da Dose Reduzida por Ano')
plt.xlabel('Ano')
plt.ylabel('Dose Média Reduzida (mg)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

print("\n📊 Média da dose reduzida por ano:")
print(media_reducao_ano)

# --------------------------------------------------------------------------------------------------------------------
# 11. Média de redução total
media_reducao_total = df_reducoes_participantes['doseareduzir'].mean()

print(f"\n📊 Média total da dose reduzida: {media_reducao_total:.2f} mg")
