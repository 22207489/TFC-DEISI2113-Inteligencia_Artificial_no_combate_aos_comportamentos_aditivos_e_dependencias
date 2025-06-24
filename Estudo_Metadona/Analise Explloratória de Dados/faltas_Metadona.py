import pandas as pd
import matplotlib.pyplot as plt

df_faltas = pd.read_csv('registo_faltas.csv')

df_faltas['timestamp'] = pd.to_datetime(df_faltas['timestamp'], errors='coerce')

# --------------------------------------------------------------------------------------------------------------------
# 1. Histograma de faltas (com números concretos nas barras)
plt.figure(figsize=(10,6))

faltas_count = df_faltas['faltas'].value_counts().sort_index()
ax = faltas_count.plot(kind='bar', color='skyblue')

plt.title('Distribuição do Número de Faltas')
plt.xlabel('Número de Faltas')
plt.ylabel('Número de Utentes')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adicionar valores por cima das barras
for i, v in enumerate(faltas_count.values):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------------------------------
# 2. Número de tomas realizadas vs não realizadas
tomas_counts = df_faltas['tomada'].value_counts().reindex([False, True])
tomas_counts.index = ['Não Tomada', 'Tomada']

plt.figure(figsize=(8,6))
ax = tomas_counts.plot(kind='bar', color='mediumseagreen')
plt.title('Número de Tomas de Recuperação Realizadas vs Não Realizadas')
plt.xlabel('Status da Toma')
plt.ylabel('Quantidade')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adicionar valores
for i, v in enumerate(tomas_counts.values):
    plt.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------------------------------
# 3. Distribuição dos valores administrados por toma
plt.figure(figsize=(10,6))
df_faltas['valor_desta_toma'].dropna().astype(float).plot(kind='hist', bins=20, color='coral', edgecolor='black')
plt.title('Distribuição dos Valores a Recuperar por Toma')
plt.xlabel('Valor da Toma')
plt.ylabel('Número de Registos')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------------------------------
# 4. Média de faltas por utente (normal)
faltas_por_utente = df_faltas.groupby('utente')['faltas'].first()
media_faltas = faltas_por_utente.mean()

print(f"\n📊 Média geral de faltas por utente: {media_faltas:.2f}")

# --------------------------------------------------------------------------------------------------------------------
# 5. Média de faltas por utente por ano
df_faltas['ano'] = df_faltas['timestamp'].dt.year
faltas_por_utente_ano = df_faltas.groupby(['ano', 'utente'])['faltas'].first()
media_faltas_por_ano = faltas_por_utente_ano.groupby('ano').mean()

print("\n📊 Média de faltas por utente por ano:")
print(media_faltas_por_ano)

# Plot da média de faltas por ano
plt.figure(figsize=(10,6))
ax = media_faltas_por_ano.plot(kind='bar', color='plum')
plt.title('Média de Faltas por Utente por Ano')
plt.xlabel('Ano')
plt.ylabel('Média de Faltas')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adicionar valores
for i, v in enumerate(media_faltas_por_ano.values):
    plt.text(i, v + 0.05, f"{v:.2f}", ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
