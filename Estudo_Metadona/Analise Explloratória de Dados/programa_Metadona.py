import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df_utentes = pd.read_csv(r"C:/TFC/EstudoMetadona/dados/utentes/utentes.csv")
df_programa = pd.read_csv("programa.csv")

# Filtrar apenas utentes no programa de metadona
df_programa_metadona = df_utentes[df_utentes['prog_metadona'] == True]
df_programa = df_programa[df_programa['utente_id'].isin(df_programa_metadona['utente_id'])]

# Corrigir datas
df_programa['entrada'] = pd.to_datetime(df_programa['entrada'], errors='coerce')
df_programa['saida'] = pd.to_datetime(df_programa['saida'], errors='coerce')

# Mapeamento
origem_map = {
    20: 'CAT', 21: 'Centro Acolhimento', 22: 'Colaboração', 23: 'CT', 24: 'EIT',
    25: 'EP', 26: 'Equipa de Rua', 28: 'GAT - Av. Ceuta', 29: 'GAT Ocidental',
    30: 'GAT Oriental', 31: 'Iniciativa Própria', 32: 'Instituição de Saúde',
    33: 'Intendente', 34: 'Lumiar', 35: 'Outro', 36: 'UM - VITAE',
    37: 'Unidade Móvel 1', 38: 'Unidade Móvel 2'
}

motivo_map = {
    20: 'Abandono', 21: 'Alta', 22: 'CAT', 23: 'Centro Acolhimento', 24: 'Colaboração',
    25: 'CT', 26: 'EP', 27: 'Exclusão', 28: 'Falecimento', 29: 'Lumiar',
    30: 'Outro', 31: 'Unidade Móvel 1', 32: 'Unidade Móvel 2'
}

df_programa['origem_nome'] = df_programa['origem_id'].map(origem_map)
df_programa['motivo_nome'] = df_programa['motivo_id'].map(motivo_map)

# --------------------------------------------------------------------------------------------------------------------
# 1. Entradas por ano
plt.figure(figsize=(10,6))
entradas_ano = df_programa['entrada'].dt.year.value_counts().sort_index()
ax = entradas_ano.plot(kind='bar', color='skyblue')
plt.title('Número de entradas de utentes por ano')
plt.xlabel('Ano')
plt.ylabel('Número de Utentes')
for i, v in enumerate(entradas_ano):
    ax.text(i, v + 0.5, str(v), ha='center', fontsize=9)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------------------------------
# 2. Número de saídas por ano
# 2. Número de saídas por ano (com valores concretos)
plt.figure(figsize=(10,6))

# Calcular os dados
saidas_por_ano = df_programa['saida'].dropna().dt.year.value_counts().sort_index()

# Criar o gráfico
ax = saidas_por_ano.plot(kind='bar', color='lightgreen')

# Título e eixos
plt.title('Número de Saídas por Ano')
plt.xlabel('Ano')
plt.ylabel('Número de Utentes')

# Adicionar valores por cima das barras
for i, v in enumerate(saidas_por_ano):
    ax.text(i, v + 0.5, str(v), ha='center', fontsize=9)

# Estética
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------------------------------
# 4. Motivos de saída
plt.figure(figsize=(10,6))
motivos = df_programa['motivo_nome'].value_counts()
ax = motivos.plot(kind='bar', color='mediumpurple')
plt.title('Motivos de Saída do Programa')
plt.xlabel('Motivo de Saída')
plt.ylabel('Número de Utentes')
for i, v in enumerate(motivos):
    ax.text(i, v + 0.5, str(v), ha='center', fontsize=9)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------------------------------
# 6. Origem dos utentes
plt.figure(figsize=(10,6))
origens = df_programa['origem_nome'].value_counts()
ax = origens.plot(kind='bar', color='gold')
plt.title('Distribuição da Origem dos Utentes')
plt.xlabel('Origem')
plt.ylabel('Número de Utentes')
for i, v in enumerate(origens):
    ax.text(i, v + 0.5, str(v), ha='center', fontsize=9)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------------------------------
# 7. Número de utentes que voltaram a entrar
reentradas = df_programa['utente_id'].value_counts()
utentes_reentraram = reentradas[reentradas > 1].count()
print(f"🔁 Número de utentes que voltaram a marcar entrada: {utentes_reentraram}")

# --------------------------------------------------------------------------------------------------------------------
# 8. Número de utentes que saíram por alta e voltaram
utentes_alta = df_programa[df_programa['motivo_nome'] == 'Alta']['utente_id']
utentes_alta_reentraram = utentes_alta[utentes_alta.isin(reentradas[reentradas > 1].index)]
numero_utentes_alta_reentraram = utentes_alta_reentraram.nunique()
print(f"📊 Número de utentes que saíram por alta e voltaram a entrar: {numero_utentes_alta_reentraram}")

# --------------------------------------------------------------------------------------------------------------------
# 9. Percentagem de sucesso
utentes_alta_sem_reentrada = utentes_alta[~utentes_alta.isin(reentradas[reentradas > 1].index)]
numero_sem_reentrada = utentes_alta_sem_reentrada.nunique()
total_utentes_alta = utentes_alta.nunique()
percentagem_sucesso = (numero_sem_reentrada / total_utentes_alta) * 100
print(f"✅ Percentagem de sucesso de saída por alta (sem retorno): {percentagem_sucesso:.2f}%")
print(f"({numero_sem_reentrada} de {total_utentes_alta} utentes)")
