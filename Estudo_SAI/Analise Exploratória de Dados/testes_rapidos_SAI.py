import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar dados
df_utentes = pd.read_csv(r"C:/TFC/SAI/dados/utentes/utentes.csv")
df_testes = pd.read_csv("testes_rapidos_utentes.csv")  # Substituir pelo caminho correto

# Filtrar utentes no programa de acolhimento
df_programa = df_utentes[df_utentes['prog_consumo'] == True]

# Filtrar apenas testes dos utentes no programa
df_testes = df_testes[df_testes['utente_id'].isin(df_programa['utente_id'])]

# Mapas de valores
teste_map = {
    1: 'VIH',
    2: 'AGHBS',
    3: 'VHC',
    4: 'Sífilis',
    5: 'RnaHCV'
}

resultado_map = {
    1: 'Reativo',
    2: 'Não Reativo',
    3: 'Inconclusivo'
}

# Aplicar mapeamentos
df_testes['teste_nome'] = df_testes['teste'].map(teste_map)
df_testes['resultado_nome'] = df_testes['resultado'].map(resultado_map)

# Converter timestamp
df_testes['timestamp'] = pd.to_datetime(df_testes['timestamp'], errors='coerce')
df_testes['ano'] = df_testes['timestamp'].dt.year

# -----------------------------
# 1. Número de testes por tipo
plt.figure(figsize=(8,5))
teste_counts = df_testes['teste_nome'].value_counts().sort_index()
ax = teste_counts.plot(kind='bar', color='skyblue')
plt.title('Número de Testes Rápidos realizados por Doença (SAI)')
plt.xlabel('Tipo de Teste')
plt.ylabel('Número de Testes')
plt.xticks(rotation=45, ha='right')
for i, v in enumerate(teste_counts.values):
    plt.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=9)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# -----------------------------
# 2. Distribuição de resultados por tipo de teste
plt.figure(figsize=(10,6))
resultado_teste = df_testes.groupby(['teste_nome', 'resultado_nome']).size().unstack().fillna(0)

ax = resultado_teste.plot(kind='bar', stacked=True, colormap='Set2', figsize=(10,6))
plt.title('Resultados por Tipo de Doença (SAI)')
plt.xlabel('Tipo de Teste')
plt.ylabel('Número de Resultados')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Resultado')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# ➤ Adicionar os valores concretos nas barras
for i, idx in enumerate(resultado_teste.index):
    cumulative = 0
    for col in resultado_teste.columns:
        value = resultado_teste.loc[idx, col]
        if value > 0:
            ax.text(i, cumulative + value / 2, int(value), ha='center', va='center', fontsize=8)
            cumulative += value

plt.tight_layout()
plt.show()

# -----------------------------
# 3. Número de testes por ano
plt.figure(figsize=(8,5))
ano_counts = df_testes['ano'].value_counts().sort_index()
ax = ano_counts.plot(kind='bar', color='coral')
plt.title('Número de Testes Rápidos por Ano (SAI)')
plt.xlabel('Ano')
plt.ylabel('Número de Testes')
plt.xticks(rotation=0)
for i, v in enumerate(ano_counts.values):
    plt.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=9)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
