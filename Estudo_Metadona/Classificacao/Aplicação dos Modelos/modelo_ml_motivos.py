import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Carregar dados
df = pd.read_csv("tabela_classificacao.csv")

# 2. Escalonar colunas contínuas
colunas_escalonar = ['media_dose_reducao', 'media_periodo_reducao',
                     'num_admissoes', 'total_testes_realizados', 'doencas_positivas',
                     'num_saidas', 'n_analises_VIH', 'n_analises_AGHBS', 'n_analises_ACHBS',
                     'n_analises_ACHBC', 'n_analises_ACHCV', 'n_analises_VDRL',
                     'n_analises_TPHA', 'n_analises_RX', 'n_analises_BK',
                     'num_reducoes', 'idade', 'tempo_medio_estadia']
scaler = StandardScaler()
df[colunas_escalonar] = scaler.fit_transform(df[colunas_escalonar])

# 3. Features e target
X = df.drop(columns=['saida_sem_retorno_abandono', 'saida_sem_retorno_motivo', 'ativo_atualmente'])
y = df['saida_sem_retorno_motivo']

# Separar treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42)

# Definir modelos
modelos = {
    "Random Forest": RandomForestClassifier(
        n_estimators=500,
        max_depth=10,
        min_samples_leaf=20,
        class_weight='balanced',
        random_state=42
    ),
    "XGBoost": XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        gamma=1,
        scale_pos_weight=3,
        eval_metric='mlogloss',
        use_label_encoder=False,
        random_state=42
    )
}

# Motivos que não se quer mostrar nos gráficos
motivos_excluir = [10.0, 11.0, 12.0, 13.0]

# === Avaliação com Train/Test Split ===
print("\n=== 1️⃣ Avaliação com Train/Test Split ===")
for nome, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    # Todas as classes (inclusive as que não se quer mostrar)
    classes_todas = sorted(y.unique())
    labels_todas = [str(cl) for cl in classes_todas]

    print(f"\n{nome} - Train/Test Split")
    print(classification_report(y_test, y_pred, labels=classes_todas, target_names=labels_todas, zero_division=0))

    # Matriz de confusão completa
    matriz_completa = confusion_matrix(y_test, y_pred, labels=classes_todas)

    # Filtrar para remover as linhas/colunas correspondentes aos motivos a excluir
    classes_filtradas = [cl for cl in classes_todas if cl not in motivos_excluir]
    indices_validos = [classes_todas.index(cl) for cl in classes_filtradas]

    matriz_filtrada = matriz_completa[np.ix_(indices_validos, indices_validos)]
    labels_filtrados = [str(cl) for cl in classes_filtradas]

    # Plot matriz filtrada
    plt.figure(figsize=(8, 6))
    sns.heatmap(matriz_filtrada, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels_filtrados, yticklabels=labels_filtrados)
    plt.title(f"Matriz de Confusão - {nome} (Train/Test)")
    plt.xlabel("Previsto")
    plt.ylabel("Real")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
