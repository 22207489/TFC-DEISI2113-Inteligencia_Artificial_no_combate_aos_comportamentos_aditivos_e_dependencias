import pandas as pd

# Mostrar todas as colunas (opcional)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Carregar o ficheiro CSV com os dados de avaliações
df_avaliacoes = pd.read_csv("enfermagem_avaliacao_episodio_202505181049.csv")  # Substituir pelo nome correto se necessário

# Dicionário com os nomes das avaliações
mapa_avaliacoes = {
    1: "Avaliação Tensão arterial",
    2: "Avaliação Frequência Cardiaca/pulso",
    3: "Avaliação Frequência respiratória",
    4: "Avaliação Saturação de oxigénio",
    5: "Avaliação Temperatura",
    6: "Avaliação Glicémia",
    7: "Avaliação Dor",
    100: "Score neurológico (Escala de Comas de Glasgow)"
}

# Contagem por utente e tipo de avaliação
df_contagem = df_avaliacoes.groupby(["utente_id", "avaliacao"]).size().unstack(fill_value=0)

# Substituir os códigos pelos nomes legíveis
df_contagem.rename(columns=mapa_avaliacoes, inplace=True)

# Resetar índice para manter utente_id como coluna
df_contagem.reset_index(inplace=True)

# Ver os primeiros resultados
print(df_contagem.head())

# (Opcional) Guardar em CSV
df_contagem.to_csv("avaliacoes_por_utente.csv", index=False)
