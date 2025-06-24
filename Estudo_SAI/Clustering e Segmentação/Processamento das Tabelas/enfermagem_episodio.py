import pandas as pd

# (Opcional) Mostrar todas as colunas e linhas no output
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Carregar o ficheiro com os atos de enfermagem realizados
df_acts = pd.read_csv("enfermagem_episodio_202505181049.csv")

# Dicionário com as descrições dos atos de enfermagem
mapa_descricoes = {
    1: "Preparação de terapêutica",
    2: "Pensos",
    3: "Adm. de medicação Oral",
    4: "Adm. de medicação Intramuscular",
    5: "Adm. de medicação Endovenoso",
    6: "Adm. de medicação Subcutâneo",
    7: "Apoio à injecção",
    8: "Ensino redução danos endovenoso",
    9: "Ensino redução danos comportamentos sexuais",
    10: "Consulta de enfermagem utente",
    11: "Consulta de enfermagem comunitário",
    104: "Atuação de emergência",
    105: "Rastreio serológicos",
    106: "Monitorização",
    107: "Administração de oxigénio"
}

# Criar tabela com número de vezes que cada utente realizou cada tipo de ato
df_todos_atos = df_acts.groupby(["utente_id", "enfermagem"]).size().unstack(fill_value=0)

# Renomear colunas com os nomes dos atos
df_todos_atos.rename(columns=mapa_descricoes, inplace=True)

# Adicionar coluna com total de atos de enfermagem realizados por utente
df_todos_atos["Total_Episodios_Enfermagem"] = df_todos_atos.sum(axis=1)

# Resetar o índice para transformar utente_id numa coluna normal
df_todos_atos.reset_index(inplace=True)

# Visualizar os primeiros resultados
print(df_todos_atos.head())

# (Opcional) Guardar em ficheiro CSV
df_todos_atos.to_csv("atos_enfermagem_por_utente.csv", index=False)
