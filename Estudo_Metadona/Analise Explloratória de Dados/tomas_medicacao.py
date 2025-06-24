import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df_utentes = pd.read_csv(r"C:/TFC/EstudoMetadona/dados/utentes/utentes.csv")
df_programa = pd.read_csv("tomas_medicacao.csv")

# Filtrar apenas utentes que participam no programa de metadona
df_programa_metadona = df_utentes[df_utentes['prog_metadona'] == True]
df_programa = df_programa[df_programa['utente_id'].isin(df_programa_metadona['utente_id'])]

# Mapa de medicamentos
medicamento_map = {
    1: 'Antibacilar',
    2: 'ARV - VIH',
    3: 'VHC',
    4: 'Psiquiátrica',
    5: 'Outra'
}

# Aplicar o mapeamento
df_programa['medicamento_nome'] = df_programa['medicamento_id'].map(medicamento_map)

# --------------------------------------------------------------------------------------------------------------------
# 2. Distribuição dos Medicamentos Administrados (agora com nomes)

plt.figure(figsize=(10,6))
df_programa['medicamento_nome'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Distribuição dos Medicamentos Administrados')
plt.xlabel('Medicamento')
plt.ylabel('Número de Administrações')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------------------------------
# 4. Número de Administrações por Utente

plt.figure(figsize=(10,6))
df_programa['utente_id'].value_counts().plot(kind='hist', bins=30, color='salmon', edgecolor='black')
plt.title('Distribuição do Número de Administrações por Utente')
plt.xlabel('Número de Administrações')
plt.ylabel('Número de Utentes')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
