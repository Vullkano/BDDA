import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
import seaborn as sns

def plot_dendrogram(df_normalized, features):
    """
    Função para exibir um dendrograma com base nos dados fornecidos.
    Args:
        df_normalized: DataFrame normalizado com os dados.
        features: Lista de características para clustering.
    """
    # Matriz de ligação para o dendrograma (Método Ward)
    linked = linkage(df_normalized[features], method='ward')

    # Plot do dendrograma
    plt.figure(figsize=(10, 6))
    dendrogram(linked, orientation='top', distance_sort='ascending', show_leaf_counts=True)
    plt.title('Dendrograma - Clusterização Hierárquica (Método Ward)')
    plt.xlabel('Amostras')
    plt.ylabel('Distância Euclidiana')
    plt.show()

def apply_agglomerative_clustering(df_normalized, features, n_clusters):
    """
    Função para aplicar Agglomerative Clustering aos dados.
    Args:
        df: DataFrame original com os dados.
        df_normalized: DataFrame normalizado com os dados.
        features: Lista de características para clustering.
        n_clusters: Número de clusters desejado.
    Returns:
        df: DataFrame com a coluna 'Cluster_Hierarchical' contendo os rótulos dos clusters.
    """
    # Agglomerative Clustering com o método Ward
    agglomerative = AgglomerativeClustering(n_clusters=n_clusters, metric='euclidean', linkage='ward')
    df_normalized['Cluster_Hierarchical'] = agglomerative.fit_predict(df_normalized[features])

    return df_normalized

def plot_cluster_characteristics(df, features, cluster_column):
    """
    Gera um barplot com as médias das características para cada cluster.
    Args:
        df: DataFrame com os dados e rótulos de cluster.
        features: Lista de características analisadas.
        cluster_column: Nome da coluna contendo os rótulos dos clusters.
    """
    # Cálculo das médias das características por cluster
    cluster_means = df.groupby(cluster_column)[features].mean().reset_index()

    # Reformata os dados para visualização
    melted = cluster_means.melt(id_vars=cluster_column, var_name='Feature', value_name='Mean')

    # Plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=melted, x='Feature', y='Mean', hue=cluster_column, dodge=True)
    plt.title('Características Médias por Cluster (Dados Normalizados)')
    plt.xlabel('Características')
    plt.ylabel('Média')
    plt.legend(title='Cluster')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def normalize_dataframe(df, features):
    """
    Normaliza as colunas selecionadas de um DataFrame usando StandardScaler.
    Args:
        df: DataFrame original.
        features: Lista de colunas a serem normalizadas.
    Returns:
        df_normalized: DataFrame com as colunas normalizadas.
    """
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[features])
    df_normalized = pd.DataFrame(df_scaled, columns=features, index=df.index)
    return df_normalized

if __name__ == "__main__":
    # Exemplo de uso com dados de música (track data)
    df = pd.DataFrame({
        'track_id': [1, 2, 3, 4, 5],
        'name': ['track1', 'track2', 'track3', 'track4', 'track5'],
        'danceability': [0.7, 0.8, 0.9, 0.65, 0.75],
        'energy': [0.6, 0.7, 0.8, 0.55, 0.75],
        'acousticness': [0.1, 0.2, 0.3, 0.05, 0.15],
        'valence': [0.5, 0.6, 0.7, 0.55, 0.65],
        'tempo': [120, 130, 140, 125, 135],
        'duration_ms': [200000, 250000, 300000, 220000, 270000],
        'release_date': ['2011-02-08', '2001', '2020-11-15', '2015-03-10', '2019-07-21'],
        'year': [2011, 2001, 2020, 2015, 2019],
        'month': [2, 5, 11, 3, 7]
    })

    # Seleção de colunas para normalizar
    features = ['danceability', 'energy', 'acousticness', 'valence', 'tempo', 'duration_ms']

    # Normalizar as colunas selecionadas
    df_normalized = normalize_dataframe(df, features)

    # Exibir o DataFrame normalizado
    print("DataFrame Normalizado:")
    print(df_normalized)

    # 1. Exibir dendrograma com o DataFrame normalizado
    plot_dendrogram(df_normalized, features)

    # 2. Aplicar Agglomerative Clustering com o DataFrame normalizado
    n_clusters = 3  # Número de clusters escolhido após análise do dendrograma
    df_normalized = apply_agglomerative_clustering(df_normalized, features, n_clusters)

    # 3. Plot das características médias por cluster (dados normalizados)
    plot_cluster_characteristics(df_normalized, features, 'Cluster_Hierarchical')

    # **ADICIONANDO A COLUNA DE CLUSTERS NO DATAFRAME ORIGINAL**
    df['Cluster_Hierarchical'] = df_normalized['Cluster_Hierarchical']

    # Exibir o DataFrame original com a coluna de clusters
    print("\nDataFrame Original com a Coluna 'Cluster_Hierarchical':")
    print(df)
