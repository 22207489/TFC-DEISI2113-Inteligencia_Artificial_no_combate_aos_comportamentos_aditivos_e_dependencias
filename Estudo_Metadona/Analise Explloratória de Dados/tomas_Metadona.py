import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Carregar os dados
df_programa = pd.read_csv("tomas.csv")

# Datas e mapeamentos
df_programa['data'] = pd.to_datetime(df_programa['data'], errors='coerce')
df_programa['datahora_registo'] = pd.to_datetime(df_programa['datahora_registo'], errors='coerce')

unidade_movel_map = {
    1: 'UM1',
    2: 'UM2',
    3: 'Lumiar',
    4: 'CA1'
}
df_programa['unidade_movel_nome'] = df_programa['um'].map(unidade_movel_map)
df_programa['hora'] = df_programa['datahora_registo'].dt.hour
df_programa['ano'] = df_programa['datahora_registo'].dt.year

# 1. Movimentação por Hora
plt.figure(figsize=(10,6))
mov_hora = df_programa['hora'].value_counts().sort_index()
ax = mov_hora.plot(kind='bar', color='skyblue')
plt.title('Número de administrações de tomas por horas do dia')
plt.xlabel('Hora do Dia')
plt.ylabel('Número de Administrações')
for i, v in enumerate(mov_hora):
    ax.text(i, v + 1, str(v), ha='center', fontsize=8)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 2. Doses por Ano
plt.figure(figsize=(10,6))
doses_ano = df_programa['data'].dt.year.value_counts().sort_index()
ax = doses_ano.plot(kind='bar', color='lightgreen')
plt.title('Número de doses de metadona administradas por ano')
plt.xlabel('Ano')
plt.ylabel('Número de Doses')
for i, v in enumerate(doses_ano):
    ax.text(i, v + 1, str(v), ha='center', fontsize=8)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 3. Dose média geral por utente
df_tomadas = df_programa[(df_programa['dose'].notna()) & (df_programa['id_status'] == 't')]
media_dose_por_utente = df_tomadas.groupby('id_utente')['dose'].mean()
media_dose_geral = media_dose_por_utente.mean()
print(f"✅ Dose média tomada por utente (geral): {media_dose_geral:.2f} mg")

# 4. Dose média por ano
media_dose_ano = df_tomadas.groupby('ano')['dose'].mean()
plt.figure(figsize=(10,6))
ax = media_dose_ano.plot(kind='line', marker='o', color='crimson')
plt.title('Dose média tomada de metadona por ano')
plt.xlabel('Ano')
plt.ylabel('Dose Média (mg)')
plt.xticks(media_dose_ano.index)
for x, y in zip(media_dose_ano.index, media_dose_ano.values):
    ax.text(x, y + 0.5, f"{y:.1f}", ha='center', fontsize=8)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 5. Utentes únicos por unidade móvel
utentes_por_um = df_programa.groupby('unidade_movel_nome')['id_utente'].nunique().sort_values(ascending=False)
plt.figure(figsize=(10,6))
ax = utentes_por_um.plot(kind='bar', color='mediumpurple')
plt.title('Número de Utentes por Unidade Móvel')
plt.xlabel('Unidade Móvel')
plt.ylabel('Número de Utentes Únicos')
for i, v in enumerate(utentes_por_um):
    ax.text(i, v + 0.5, str(v), ha='center', fontsize=8)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 6. Heatmap hora x unidade móvel
df_horas_um = df_programa.groupby(['unidade_movel_nome', 'hora']).size().reset_index(name='contagem')
pivot_horas_um = df_horas_um.pivot(index='unidade_movel_nome', columns='hora', values='contagem')
plt.figure(figsize=(14,8))
sns.heatmap(pivot_horas_um.fillna(0), cmap='YlGnBu', linewidths=0.5, annot=True, fmt='.0f')
plt.title('Movimentação por Hora em cada Unidade Móvel')
plt.xlabel('Hora do Dia')
plt.ylabel('Unidade Móvel')
plt.tight_layout()
plt.show()

# 7. Movimentação por hora ao longo dos anos por unidade móvel
df_grouped = df_programa.groupby(['unidade_movel_nome', 'ano', 'hora']).size().reset_index(name='contagem')
unidades = df_grouped['unidade_movel_nome'].unique()

for unidade in unidades:
    df_unidade = df_grouped[df_grouped['unidade_movel_nome'] == unidade]
    plt.figure(figsize=(14,8))
    for ano in sorted(df_unidade['ano'].dropna().unique()):
        df_ano = df_unidade[df_unidade['ano'] == ano]
        plt.plot(df_ano['hora'], df_ano['contagem'], marker='o', label=f'{int(ano)}')
        for x, y in zip(df_ano['hora'], df_ano['contagem']):
            plt.text(x, y + 0.5, str(y), ha='center', fontsize=7)
    plt.title(f'Movimentação por Hora do Dia ao Longo dos Anos - {unidade}')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Número de Administrações')
    plt.xticks(range(0, 24))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Ano')
    plt.tight_layout()
    plt.show()
