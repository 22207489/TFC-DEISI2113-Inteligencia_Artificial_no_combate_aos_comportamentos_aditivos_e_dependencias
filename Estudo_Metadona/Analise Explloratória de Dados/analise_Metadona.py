import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df_utentes = pd.read_csv(r"C:/TFC/EstudoMetadona/dados/utentes/utentes.csv")
df_analises = pd.read_csv("analises_feitas.csv")

# Filtrar utentes no programa
df_metadona = df_utentes[df_utentes['prog_metadona'] == True]
df_analises_metadona = df_analises[df_analises['utente_id'].isin(df_metadona['utente_id'])]

# Mapas
analise_map = {
    1: 'VIH', 2: 'AGHBS', 3: 'ACHBS', 4: 'ACHBC', 5: 'ACHCV',
    6: 'VDRL', 7: 'TPHA', 8: 'RX', 9: 'BK'
}

# Casos positivos por doença
df_positivos = df_analises_metadona[df_analises_metadona['resultado'] == 'p']
analise_counts = df_positivos['analise'].value_counts().sort_index()
analise_counts.index = analise_counts.index.map(analise_map)

plt.figure(figsize=(10, 6))
ax = analise_counts.plot(kind='bar', color='crimson')
plt.title('Número de Utentes com Resultado Positivo por Tipo de Análise')
plt.xlabel('Análise')
plt.ylabel('Nº de Resultados Positivos')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, v in enumerate(analise_counts.values):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Casos positivos por ano
df_analises_metadona['data'] = pd.to_datetime(df_analises_metadona['data'], errors='coerce')
df_positivos = df_analises_metadona[df_analises_metadona['resultado'] == 'p']
df_positivos['ano'] = df_positivos['data'].dt.year
positivos_por_ano = df_positivos['ano'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
ax = positivos_por_ano.plot(kind='bar', color='mediumseagreen')
plt.title('Número de Casos Positivos por Ano no Estudo de Metadonai9o')
plt.xlabel('Ano')
plt.ylabel('Número de Casos Positivos')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, v in enumerate(positivos_por_ano.values):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Número total de análises por ano
df_analises_metadona['ano'] = df_analises_metadona['data'].dt.year
analises_por_ano = df_analises_metadona['ano'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
ax = analises_por_ano.plot(kind='bar', color='steelblue')
plt.title('Número Total de Análises por Ano no Estudo de Metadona')
plt.xlabel('Ano')
plt.ylabel('Número de Análises')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, v in enumerate(analises_por_ano.values):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# Totais gerais
total_analises = len(df_analises_metadona)
total_positivos = len(df_analises_metadona[df_analises_metadona['resultado'] == 'p'])

print(f"Total de análises feitas: {total_analises}")
print(f"Total de casos positivos: {total_positivos}")

# Proporção de positivos por tipo
total_por_tipo = df_analises_metadona['analise'].value_counts().sort_index()
positivos_por_tipo = df_analises_metadona[df_analises_metadona['resultado'] == 'p']['analise'].value_counts().sort_index()
proporcao_positivos = (positivos_por_tipo / total_por_tipo) * 100
proporcao_positivos.index = proporcao_positivos.index.map(analise_map)

plt.figure(figsize=(10, 6))
ax = proporcao_positivos.plot(kind='bar', color='darkorange')
plt.title('Proporção de Casos Positivos por Tipo de Análise no Estudo de Metadona (%)')
plt.xlabel('Análise')
plt.ylabel('Percentagem de Casos Positivos')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, v in enumerate(proporcao_positivos.values):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Total de exames por tipo
total_por_tipo.index = total_por_tipo.index.map(analise_map)

plt.figure(figsize=(10, 6))
ax = total_por_tipo.plot(kind='bar', color='mediumpurple')
plt.title('Distribuição do Número de Exames por Tipo')
plt.xlabel('Análise')
plt.ylabel('Número de Exames')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, v in enumerate(total_por_tipo.values):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.show()
