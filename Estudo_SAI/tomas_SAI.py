import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
df = pd.read_csv("tomas_medicacao.csv")
# substitui pelo caminho correto
# Dicionário de medicamentos
medicamento_map = {
    1: 'Antibacilar',
    2: 'ARV - VIH',
    3: 'VHC',
    4: 'Psiquiátrica',
    5: 'Outra'
}

# Aplicar mapeamento
df['medicamento_nome'] = df['medicamento_id'].map(medicamento_map)
df['data'] = pd.to_datetime(df['data'], errors='coerce')
df['ano'] = df['data'].dt.year

# 1. Gráfico de tipos de medicamento
plt.figure(figsize=(8, 5))
counts = df['medicamento_nome'].value_counts().sort_index()
ax = counts.plot(kind='bar', color='skyblue')
plt.title('Número de Administrações por Tipo de Medicamento no SAI')
plt.xlabel('Tipo de Medicamento')
plt.ylabel('Número de Administrações')
plt.xticks(rotation=45, ha='right')
for i, v in enumerate(counts.values):
    plt.text(i, v + (v * 0.01), str(v), ha='center', va='bottom', fontsize=9)  # ajuste aqui
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 2. Gráfico de administrações por enfermeiro
plt.figure(figsize=(8, 5))
counts_enf = df['enfermeiro_id'].value_counts().sort_index()
ax = counts_enf.plot(kind='bar', color='lightgreen')
plt.title('Número de Administrações de Medicamentos por Enfermeiro no SAI')
plt.xlabel('ID do Enfermeiro')
plt.ylabel('Número de Administrações')
plt.xticks(rotation=0)
for i, v in enumerate(counts_enf.values):
    plt.text(i, v + (v * 0.01), str(v), ha='center', va='bottom', fontsize=8)  # ajuste aqui
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 3. Gráfico de administrações por ano
plt.figure(figsize=(8, 5))
counts_ano = df['ano'].value_counts().sort_index()
ax = counts_ano.plot(kind='bar', color='salmon')
plt.title('Distribuição de Administrações de Medicamentos por Ano no SAI')
plt.xlabel('Ano')
plt.ylabel('Número de Administrações')
plt.xticks(rotation=0)
for i, v in enumerate(counts_ano.values):
    plt.text(i, v + (v * 0.01), str(v), ha='center', va='bottom', fontsize=8)  # ajuste aqui
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
