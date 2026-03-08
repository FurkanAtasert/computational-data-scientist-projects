import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Load dataset
data = pd.read_excel("project_dataset.xlsx")

# Create subset from AGE_GROUP and HB columns
subset = data[['AGE_GROUP', 'HB']]

# Scale data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(subset)

# Train / Test split
X_train, X_test = train_test_split(scaled_data, test_size=0.2, random_state=42)

np.random.seed(42)

def custom_kmeans(X, n_clusters, max_iters=100):

    centers = X[np.random.choice(range(len(X)), size=n_clusters, replace=False)]

    for _ in range(max_iters):

        labels = np.argmin(np.linalg.norm(X[:, np.newaxis] - centers, axis=2), axis=1)

        new_centers = np.array([X[labels == i].mean(axis=0) for i in range(n_clusters)])

        if np.allclose(centers, new_centers):
            break

        centers = new_centers

    return labels


def simple_neural_network(X, n_clusters, max_iters=100):

    weights = np.random.rand(n_clusters, X.shape[1])

    for _ in range(max_iters):

        closest_center_indices = np.argmin(np.linalg.norm(X[:, np.newaxis] - weights, axis=2), axis=1)

        for i in range(n_clusters):
            if np.any(closest_center_indices == i):
                weights[i] = np.mean(X[closest_center_indices == i], axis=0)

    labels = np.argmin(np.linalg.norm(X[:, np.newaxis] - weights, axis=2), axis=1)

    return labels


# Run clustering algorithms
train_labels_kmeans = custom_kmeans(X_train, n_clusters=3)
test_labels_kmeans = custom_kmeans(X_test, n_clusters=3)

train_labels_snn = simple_neural_network(X_train, n_clusters=3)
test_labels_snn = simple_neural_network(X_test, n_clusters=3)


# Silhouette scores
silhouette_score_kmeans_train = silhouette_score(X_train, train_labels_kmeans)
silhouette_score_kmeans_test = silhouette_score(X_test, test_labels_kmeans)

silhouette_score_snn_train = silhouette_score(X_train, train_labels_snn)
silhouette_score_snn_test = silhouette_score(X_test, test_labels_snn)


print("K-Means Silhouette Score (Train):", silhouette_score_kmeans_train)
print("K-Means Silhouette Score (Test):", silhouette_score_kmeans_test)

print("SNN Silhouette Score (Train):", silhouette_score_snn_train)
print("SNN Silhouette Score (Test):", silhouette_score_snn_test)


# Compare algorithms
if silhouette_score_kmeans_train > silhouette_score_snn_train:
    print("K-Means performs better on the training set.")
elif silhouette_score_kmeans_train < silhouette_score_snn_train:
    print("SNN performs better on the training set.")
else:
    print("Both algorithms perform equally on the training set.")


if silhouette_score_kmeans_test > silhouette_score_snn_test:
    print("K-Means performs better on the test set.")
elif silhouette_score_kmeans_test < silhouette_score_snn_test:
    print("SNN performs better on the test set.")
else:
    print("Both algorithms perform equally on the test set.")


# Visualization
silhouette_scores_train = [silhouette_score_kmeans_train, silhouette_score_snn_train]
silhouette_scores_test = [silhouette_score_kmeans_test, silhouette_score_snn_test]

algorithms = ['K-Means', 'SNN']

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.bar(algorithms, silhouette_scores_train)
plt.title("Silhouette Score (Train)")
plt.ylabel("Score")

plt.subplot(1,2,2)
plt.bar(algorithms, silhouette_scores_test)
plt.title("Silhouette Score (Test)")
plt.ylabel("Score")

plt.tight_layout()
plt.show()


# Assign variables
age_group_train = X_train[:,0]
hb_train = X_train[:,1]

age_group_test = X_test[:,0]
hb_test = X_test[:,1]


# K-Means visualization
plt.figure(figsize=(12,6))

plt.subplot(1,2,1)
plt.scatter(age_group_train, hb_train, c=train_labels_kmeans, cmap='viridis', alpha=0.5)
plt.title("K-Means Clustering Results (Train Set)")
plt.xlabel("Age Group")
plt.ylabel("HB")

plt.subplot(1,2,2)
plt.scatter(age_group_test, hb_test, c=test_labels_kmeans, cmap='viridis', alpha=0.5)
plt.title("K-Means Clustering Results (Test Set)")
plt.xlabel("Age Group")
plt.ylabel("HB")

plt.tight_layout()
plt.show()


# SNN visualization
plt.figure(figsize=(12,6))

plt.subplot(1,2,1)
plt.scatter(age_group_train, hb_train, c=train_labels_snn, cmap='viridis', alpha=0.5)
plt.title("SNN Clustering Results (Train Set)")
plt.xlabel("Age Group")
plt.ylabel("HB")

plt.subplot(1,2,2)
plt.scatter(age_group_test, hb_test, c=test_labels_snn, cmap='viridis', alpha=0.5)
plt.title("SNN Clustering Results (Test Set)")
plt.xlabel("Age Group")
plt.ylabel("HB")

plt.tight_layout()
plt.show()