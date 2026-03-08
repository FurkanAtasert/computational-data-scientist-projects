import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from minisom import MiniSom
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Create a two-dimensional dataset
X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

# Apply the k-means algorithm
kmeans = KMeans(n_clusters=4)
kmeans.fit(X)
kmeans_centers = kmeans.cluster_centers_
kmeans_labels = kmeans.labels_
kmeans_score = silhouette_score(X, kmeans_labels)

# Apply the SNN algorithm
som = MiniSom(2, 2, 2, sigma=0.5, learning_rate=0.5)
som.random_weights_init(X)
som.train_random(X, 100)
snn_centers = som.get_weights()
snn_labels = np.array([som.winner(x)[0] for x in X])
snn_score = silhouette_score(X, snn_labels)

# Apply dimensionality reduction techniques
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)

# Visualize the results
plt.figure(figsize=(18, 8))

# K-Means visualizations
plt.subplot(2, 4, 1)
plt.scatter(X[:, 0], X[:, 1], c=kmeans_labels, cmap='viridis')
plt.scatter(kmeans_centers[:, 0], kmeans_centers[:, 1], marker='x', c='red', s=200, label='K-Means Centers')
plt.title('K-Means')
plt.legend()

plt.subplot(2, 4, 5)
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans_labels, cmap='viridis')
plt.title('PCA - K-Means')

plt.subplot(2, 4, 6)
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=kmeans_labels, cmap='viridis')
plt.title('t-SNE - K-Means')

# SNN visualizations
plt.subplot(2, 4, 2)
plt.scatter(X[:, 0], X[:, 1], c=snn_labels, cmap='viridis')
plt.scatter(snn_centers[:, :, 0], snn_centers[:, :, 1], marker='x', c='red', s=200, label='SNN Centers')
plt.title('Self-Organizing Neural Network (SNN)')
plt.legend()

plt.subplot(2, 4, 7)
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=snn_labels, cmap='viridis')
plt.title('PCA - SNN')

plt.subplot(2, 4, 8)
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=snn_labels, cmap='viridis')
plt.title('t-SNE - SNN')

plt.show()

# Display results in the terminal
print("K-Means Silhouette Score: %", f"{kmeans_score * 100}")
print("SNN Silhouette Score: %", f"{snn_score * 100}")