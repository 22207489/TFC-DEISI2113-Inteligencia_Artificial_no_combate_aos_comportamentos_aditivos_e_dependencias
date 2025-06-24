import pandas as pd
from datetime import datetime
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# === Carregamento ===
df = pd.read_csv("tabela_unificada_base_metadona.csv", low_memory=False)

# === Criar variável 'idade'
data_atual = pd.to_datetime("today")
df["data_nascimento"] = pd.to_datetime(df["utente_nascimento"], errors="coerce")
df["idade"] = ((data_atual - df["data_nascimento"]).dt.days / 365.25).round()

# === Binarização de nacionalidade e terapeuta
df["nacionalidade_portuguesa"] = df["utente_nacionalidade"].apply(lambda x: 1 if x == 620 else 0)
df["tem_terapeuta"] = df["utente_terapeuta"].notna().astype(int)
df["utente_sexo"] = df["utente_sexo"].apply(lambda x: 0 if pd.isna(x) or x == 1 else 1)




df["utente_tem_equipatratamento"] = df["utente_equipatratamento"].apply(lambda x: 1 if x>0 else 0)
df["esta_prog_consumo"] = df["prog_consumo"].apply(lambda x: 1 if x is True else 0)
df["utente_selecionado"] = df["utente_selecionado"].apply(lambda x: 1 if True else 0)
df["utente_tem_medicoassistente"] = df["utente_medicoassistente"].notnull().astype(int)
df["utente_centrosaude"] = df["utente_centrosaude"].notnull().astype(int)
df["utente_numprocesso"] = df["utente_numprocesso"].notnull().astype(int)
df["utente_fthc"] = df["utente_fthc"].apply(lambda x: 1 if x is True else 0)
df["utente_outramed"] = df["utente_outramed"].apply(lambda x: 1 if x is True else 0)

def classificarConcelho(valor):
    if 9 <= valor <= 32:
        return 1 #(Lisboa)
    elif (33 <= valor <= 39) or (41 <= valor <= 49) or (1 <= valor <= 8):
        return 2 #(Fora Lisboa)
    elif valor == 40 or valor == 42:
        return 3 #(Sem Abrigo)
    else:
        return 4  #(Sem concelho associado)

df["utente_concelhoresidencia"] = df["utente_concelhoresidencia"].apply(classificarConcelho)



# === Apagar colunas substituídas
df.drop(columns=["utente_nascimento", "utente_nacionalidade", "utente_terapeuta","utente_equipatratamento","prog_consumo","utente_medicoassistente"], inplace=True)

# === Apagar colunas com mais de 80% de nulls
percentagem_nulls = df.isnull().mean() * 100
print(percentagem_nulls)
colunas_a_remover_nulls = percentagem_nulls[percentagem_nulls > 70].index.tolist()
df.drop(columns=colunas_a_remover_nulls, inplace=True)

# === Apagar colunas irrelevantes para classificação
colunas_inuteis_para_classificacao = [
    "id_x", "utente_id", "utente_doseareduzir", "utente_periodicidade", "utente_limite",
    "utente_datareducao", "utente_obsemreducao", "utente_obs", "prog_metadona", "data_nascimento",
    "utente_emreducao", "utente_nome", "utente_cartaoutente","utente_activo"
]
colunas_presentes_para_remover = [col for col in colunas_inuteis_para_classificacao if col in df.columns]
df.drop(columns=colunas_presentes_para_remover, inplace=True)

df = df[df['idade'] >= 18]



#Remover Linhas onde nao temos entrada no programa
coluna = "saida_sem_retorno_abandono"
df = df[df[coluna].notna()]


#Preenchimento de nulls
colunas_media_arredondada = [
    'utente_local', 'utente_um', 'num_reducoes',
    'media_dose_reducao', 'media_periodo_reducao',

]

for coluna in colunas_media_arredondada:
    media = round(df[coluna].mean())
    df[coluna].fillna(media, inplace=True)


colunas_testes = [
    'n_analises_VIH', 'n_analises_AGHBS', 'n_analises_ACHBS',
    'n_analises_ACHBC', 'n_analises_ACHCV', 'n_analises_VDRL',
    'n_analises_TPHA', 'n_analises_RX', 'n_analises_BK'
]

# Criar nova coluna com a soma dos testes por utente
df['total_testes_realizados'] = df[colunas_testes].sum(axis=1)


colunas_testes = [
    'VIH_positivo', 'AGHBS_positivo', 'ACHBS_positivo',
    'ACHBC_positivo', 'ACHCV_positivo', 'VDRL_positivo',
    'TPHA_positivo', 'RX_positivo', 'BK_positivo'
]

# Criar nova coluna com a soma dos testes por utente
df['doencas_positivas'] = df[colunas_testes].sum(axis=1)


df.fillna(0, inplace=True)










# === Guardar e mostrar
df.to_csv("tabela_classificacao.csv", index=False)
print("✅ Tabela limpa e pronta para classificação.")
