import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np

# Passo 1: Carregar os dados e guardar cópia dos valores reais
df = pd.read_csv("SAI_final.csv")
df = df.fillna(0)
df_original = df.copy()  # <-- Cópia dos dados originais para análise posterior

# Passo 2: Identificar colunas binárias
colunas_binarias = [col for col in df.columns if df[col].dropna().isin([0, 1]).all()]

# Passo 3: Escalonar as colunas não-binárias
colunas_escalar = [
    'ANALISES_ACHBC', 'ANALISES_ACHBS', 'ANALISES_ACHCV', 'ANALISES_AGHBS', 'ANALISES_BK', 'ANALISES_RX',
    'ANALISES_TPHA', 'ANALISES_VDRL', 'ANALISES_VIH', 'Total_Analises',
    'HEROINA_FUMADA', 'COCAINA_FUMADA', 'HEROINA_COCAINA_FUMADAS', 'BZD_FUMADA', 'METADONA_FUMADA',
    'OUTRO_FUMADA', 'HEROINA_INJETADA', 'COCAINA_INJETADA', 'HEROINA_COCAINA_INJETADAS',
    'OUTRA_SUBSTANCIA_INJETADA', 'Pe', 'Perna', 'Inguinal', 'Braco_Antebraco',
    'KITS_IV', 'SERINGA_23G', 'SERINGA_25G', 'SERINGA_26G', 'AGUA', 'FILTRO',
    'TOALHETE', 'CACHIMBO_1', 'CACHIMBO_2', 'PRATA', 'RECIPIENTE', 'DEVOLUCAO_MATERIAL',
    'PRESERVATIVO_EXTERNO', 'PRESERVATIVO_INTERNO', 'SERINGA_29G',
    'total_episodios', 'idade'
]
scaler = StandardScaler()
df[colunas_escalar] = scaler.fit_transform(df[colunas_escalar])

# Passo 4: PCA para análise da variância explicada
pca_full = PCA(n_components=None)
pca_full.fit(df)
cum_exp_var = np.cumsum(pca_full.explained_variance_ratio_)

plt.figure(figsize=(8, 5))
plt.plot(range(1, len(cum_exp_var) + 1), cum_exp_var, marker='o')
plt.title('Variância Explicada Acumulada')
plt.xlabel('Número de Componentes')
plt.ylabel('Variância Explicada Acumulada')
plt.axhline(y=0.85, color='r', linestyle='--', label='85% Variância')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Passo 5: Número ideal de componentes
k_pca = np.argmax(cum_exp_var >= 0.85) + 1
print(f"Número de componentes selecionado: {k_pca}")

# Passo 6: Aplicar PCA
pca_final = PCA(n_components=k_pca)
df_pca = pca_final.fit_transform(df)
df_pca = pd.DataFrame(df_pca, columns=[f"PC{i+1}" for i in range(k_pca)])

# Passo 7: Elbow Method para determinar k
inertia = []
range_k = range(2, 10)

for k in range_k:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_pca)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(range_k, inertia, marker='o')
plt.title('Elbow Method')
plt.xlabel('k')
plt.ylabel('Inércia')

# Passo 8: Clustering final com KMeans
k_final = 4
kmeans = KMeans(n_clusters=k_final, random_state=42)
df['cluster'] = kmeans.fit_predict(df_pca)
df_original['cluster'] = df['cluster']  # Copiar clusters para os dados reais

# Passo 9: Visualização com centróides
centroids = kmeans.cluster_centers_

plt.figure(figsize=(6, 5))
sns.scatterplot(x=df_pca['PC1'], y=df_pca['PC2'], hue=df['cluster'], palette='Set2')
plt.scatter(centroids[:, 0], centroids[:, 1], c='black', s=150, marker='X', label='Centróides')
plt.title("Clusters com PCA (PC1 vs PC2)")
plt.legend()
plt.tight_layout()
plt.show()

# Passo 10: Análise real dos clusters com dados não transformados
resumo_reais = df_original.groupby('cluster').mean().T.round(1)
resumo_reais.to_excel("resumo_clusters_valores_reais.xlsx")

print("\n✅ Ficheiro 'resumo_clusters_valores_reais.xlsx' criado com médias reais por cluster.")
print("\n📌 Principais variáveis por cluster (com valores reais):")

for cluster_id in sorted(df_original['cluster'].unique()):
    print(f"\n🔹 Cluster {cluster_id}:")
    top_vars = resumo_reais[cluster_id].sort_values(ascending=False)
    for var, val in top_vars.items():
        print(f"  - {var}: média ≈ {val}")