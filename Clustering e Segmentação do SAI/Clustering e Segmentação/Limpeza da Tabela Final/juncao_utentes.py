import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# Carregar as duas tabelas
df1 = pd.read_csv("utentes_SAI.csv")  # Tabela principal
df2 = pd.read_csv("dataset_final_utentes.csv")  # Tabela com novas features

# Fazer merge apenas com utentes que existem na primeira tabela (left join)
df_merged = pd.merge(df1, df2, on="utente_id", how="left")
percentagem_nulos = df_merged.isnull().mean() * 100
print(percentagem_nulos[percentagem_nulos > 0].sort_values(ascending=False))

# === Criar variável 'idade'
data_atual = pd.to_datetime("today")
df_merged["data_nascimento"] = pd.to_datetime(df_merged["utente_nascimento"], errors="coerce")
df_merged["idade"] = ((data_atual - df_merged["data_nascimento"]).dt.days / 365.25).round()

#Idade superior a 18 anos
df_merged = df_merged[df_merged['idade'] >= 18]


df_merged["utente_activo"] = df_merged["utente_activo"].apply(lambda x: 1 if x is True else 0)
df_merged["utente_tem_terapeuta"] = df_merged["utente_terapeuta"].apply(lambda x: 1 if x > 0.0 else 0)
df_merged["nacionalidade_portuguesa"] = df_merged["utente_nacionalidade"].apply(lambda x: 1 if x == 620.0 else 0)
df_merged["pertence_prog_metadona"] = df_merged["prog_metadona"].apply(lambda x: 1 if x is True else 0)


df_merged["utente_tem_equipatratamento"] = df_merged["utente_equipatratamento"].apply(lambda x: 1 if x>0 else 0)
df_merged["esta_prog_consumo"] = df_merged["prog_consumo"].apply(lambda x: 1 if x is True else 0)
df_merged["utente_selecionado"] = df_merged["utente_selecionado"].apply(lambda x: 1 if x is True else 0)
df_merged["utente_tem_medicoassistente"] = df_merged["utente_medicoassistente"].notnull().astype(int)
df_merged["utente_centrosaude"] = df_merged["utente_centrosaude"].notnull().astype(int)
df_merged["utente_numprocesso"] = df_merged["utente_numprocesso"].notnull().astype(int)
df_merged["utente_fthc"] = df_merged["utente_fthc"].apply(lambda x: 1 if x is True else 0)
df_merged["utente_outramed"] = df_merged["utente_outramed"].apply(lambda x: 1 if x is True else 0)


# === Apagar colunas com mais de 80% de nulls
percentagem_nulls = df_merged.isnull().mean() * 100
colunas_a_remover_nulls = percentagem_nulls[percentagem_nulls > 80].index.tolist()
df_merged.drop(columns=colunas_a_remover_nulls, inplace=True)

colunas_a_remover = ['id', 'utente_id', 'utente_nome',
                     'utente_nascimento', 'utente_cartaoutente', 'data_prog_consumo',
                      'utente_obs',
                     'utente_criado_em', 'utente_criado_por', 'prog_consumo','data_nascimento',

                    'utente_um','utente_emreducao',
                     'utente_gravidez', 'utente_local', 'utente_opiaceos','utente_acolhimento','sem_local_injecao',
                     'utente_terapeuta','utente_nacionalidade','prog_metadona', 'ativo_atualmente','num_admissoes','num_saidas','saida_sem_retorno_binario']

# Apagar as colunas
df_merged = df_merged.drop(columns=colunas_a_remover)

df_merged = df_merged.rename(columns={'ACHBC': 'ANALISES_ACHBC'})
df_merged = df_merged.rename(columns={'ACHBS': 'ANALISES_ACHBS'})
df_merged = df_merged.rename(columns={'ACHCV': 'ANALISES_ACHCV'})
df_merged = df_merged.rename(columns={'AGHBS': 'ANALISES_AGHBS'})
df_merged = df_merged.rename(columns={'BK': 'ANALISES_BK'})
df_merged = df_merged.rename(columns={'RX': 'ANALISES_RX'})
df_merged = df_merged.rename(columns={'TPHA': 'ANALISES_TPHA'})
df_merged = df_merged.rename(columns={'VDRL': 'ANALISES_VDRL'})
df_merged = df_merged.rename(columns={'VIH': 'ANALISES_VIH'})


df_merged["ACHBC_Positivo"] = df_merged["ACHBC_Positivo"].gt(0).astype(int)
df_merged["ACHBS_Positivo"] = df_merged["ACHBS_Positivo"].gt(0).astype(int)
df_merged["ACHCV_Positivo"] = df_merged["ACHCV_Positivo"].gt(0).astype(int)
df_merged["AGHBS_Positivo"] = df_merged["AGHBS_Positivo"].gt(0).astype(int)
df_merged["BK_Positivo"] = df_merged["BK_Positivo"].gt(0).astype(int)
df_merged["RX_Positivo"] = df_merged["RX_Positivo"].gt(0).astype(int)
df_merged["TPHA_Positivo"] = df_merged["TPHA_Positivo"].gt(0).astype(int)
df_merged["VDRL_Positivo"] = df_merged["VDRL_Positivo"].gt(0).astype(int)
df_merged["VIH_Positivo"] = df_merged["VIH_Positivo"].gt(0).astype(int)




df_merged['utente_sexo'].fillna(1.0, inplace=True)
df_merged['HEROINA_FUMADA'].fillna(round(df_merged['HEROINA_FUMADA'].mean()), inplace=True)
df_merged['COCAINA_FUMADA'].fillna(round(df_merged['COCAINA_FUMADA'].mean()), inplace=True)
df_merged['HEROINA_COCAINA_FUMADAS'].fillna(round(df_merged['HEROINA_COCAINA_FUMADAS'].mean()), inplace=True)
df_merged['HEROINA_INJETADA'].fillna(round(df_merged['HEROINA_INJETADA'].mean()), inplace=True)
df_merged['COCAINA_INJETADA'].fillna(round(df_merged['COCAINA_INJETADA'].mean()), inplace=True)
df_merged['HEROINA_COCAINA_INJETADAS'].fillna(round(df_merged['HEROINA_COCAINA_INJETADAS'].mean()), inplace=True)
df_merged['Perna'].fillna(round(df_merged['Perna'].mean()), inplace=True)
df_merged['Inguinal'].fillna(round(df_merged['Inguinal'].mean()), inplace=True)
df_merged['Braco_Antebraco'].fillna(round(df_merged['Braco_Antebraco'].mean()), inplace=True)


df_merged.fillna(0, inplace=True)










# Ver as primeiras linhas (opcional)
df_merged.to_csv("SAI_final.csv", index=False)
