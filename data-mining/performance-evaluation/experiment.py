import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load dataset
data = pd.read_excel("project_dataset.xlsx")

# Create subset from AGE_GROUP and HB columns
subset = data[['AGE_GROUP', 'HB']]

# Scale data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(subset)

# Train / Test split
X_train, X_test = train_test_split(scaled_data, test_size=0.2, random_state=42)

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


# K-Means clustering
train_labels_kmeans = custom_kmeans(X_train, n_clusters=3)
test_labels_kmeans = custom_kmeans(X_test, n_clusters=3)

# SNN clustering
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


silhouette_scores_train = [silhouette_score_kmeans_train, silhouette_score_snn_train]
silhouette_scores_test = [silhouette_score_kmeans_test, silhouette_score_snn_test]

algorithms = ['K-Means', 'SNN']

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.bar(algorithms, silhouette_scores_train)
plt.title('Silhouette Score (Train)')
plt.ylabel('Silhouette Score')

plt.subplot(1, 2, 2)
plt.bar(algorithms, silhouette_scores_test)
plt.title('Silhouette Score (Test)')
plt.ylabel('Silhouette Score')

plt.tight_layout()
plt.show()


# Assign variables
age_group_train = X_train[:, 0]
hb_train = X_train[:, 1]

age_group_test = X_test[:, 0]
hb_test = X_test[:, 1]


plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
for class_value in range(3):
    row_ix = np.where(test_labels_kmeans == class_value)
    plt.scatter(age_group_test[row_ix], hb_test[row_ix], label=f'K-Means Class {class_value}')

plt.title('K-Means Clustering Results (Test Set)')
plt.xlabel('Age Group')
plt.ylabel('HB')
plt.legend()


plt.subplot(1, 3, 2)
for class_value in range(3):
    row_ix = np.where(test_labels_snn == class_value)
    plt.scatter(age_group_test[row_ix], hb_test[row_ix], label=f'SNN Class {class_value}')

plt.title('SNN Clustering Results (Test Set)')
plt.xlabel('Age Group')
plt.ylabel('HB')
plt.legend()


plt.subplot(1, 3, 3)
for class_value in range(3):
    row_ix = np.where(test_labels_kmeans == class_value)
    plt.scatter(age_group_test[row_ix], hb_test[row_ix], label=f'True Class {class_value}')

plt.title('True Classes (Test Set)')
plt.xlabel('Age Group')
plt.ylabel('HB')
plt.legend()

plt.tight_layout()
plt.show()


fig = plt.figure(figsize=(18, 6))

ax1 = fig.add_subplot(131, projection='3d')

for class_value in range(3):
    row_ix = np.where(test_labels_kmeans == class_value)
    ax1.scatter(age_group_test[row_ix], hb_test[row_ix], zs=class_value, label=f'K-Means Class {class_value}')

ax1.set_title('K-Means Clustering Results (Test Set)')
ax1.set_xlabel('Age Group')
ax1.set_ylabel('HB')
ax1.set_zlabel('Class')
ax1.legend()


ax2 = fig.add_subplot(132, projection='3d')

for class_value in range(3):
    row_ix = np.where(test_labels_snn == class_value)
    ax2.scatter(age_group_test[row_ix], hb_test[row_ix], zs=class_value, label=f'SNN Class {class_value}')

ax2.set_title('SNN Clustering Results (Test Set)')
ax2.set_xlabel('Age Group')
ax2.set_ylabel('HB')
ax2.set_zlabel('Class')
ax2.legend()


ax3 = fig.add_subplot(133, projection='3d')

for class_value in range(3):
    row_ix = np.where(test_labels_kmeans == class_value)
    ax3.scatter(age_group_test[row_ix], hb_test[row_ix], zs=class_value, label=f'True Class {class_value}')

ax3.set_title('True Classes (Test Set)')
ax3.set_xlabel('Age Group')
ax3.set_ylabel('HB')
ax3.set_zlabel('Class')
ax3.legend()

plt.tight_layout()
plt.show()