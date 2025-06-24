import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
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
y = df['saida_sem_retorno_abandono']

# 4. Separar em treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42)

# 5. Definir modelos
modelos = {
    "Regressão Logística": LogisticRegression(class_weight='balanced', max_iter=10000),
    "KNN (k=11)": KNeighborsClassifier(n_neighbors=11),
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
        eval_metric='logloss',
        random_state=42
    )
}

# === 🧪 Validação Train/Test Split ===
print("\n=== Avaliação com Train/Test Split ===")
for nome, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    print(f"\n{nome} - Train/Test Split")
    print(classification_report(y_test, y_pred, target_names=["Não Abandona", "Abandona"], zero_division=0))

    matriz = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(matriz, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Não Abandona", "Abandona"],
                yticklabels=["Não Abandona", "Abandona"])
    plt.title(f"Matriz de Confusão - {nome} (Train/Test)")
    plt.xlabel("Previsto")
    plt.ylabel("Real")
    plt.tight_layout()
    plt.show()
