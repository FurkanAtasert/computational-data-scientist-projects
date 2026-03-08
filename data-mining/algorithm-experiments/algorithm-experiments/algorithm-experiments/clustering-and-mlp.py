import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

# Load the dataset
data = pd.read_excel("sample_dataset_01.xlsx", sheet_name="Clear_Data")

# Display the first 5 rows of the dataset
print(data.head())

# Separate features and labels
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Normalize the dataset
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create and train the k-Means model
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_scaled)

# Labels produced by k-Means
kmeans_labels = kmeans.labels_

# Display k-Means results
print("k-Means Cluster Centers:\n", kmeans.cluster_centers_)
print("k-Means Labels:\n", kmeans_labels)

# Split the dataset into training and test sets for SNN
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Create and train the SNN model
snn_model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
snn_model.fit(X_train, y_train)

# Predictions from the SNN
snn_predictions = snn_model.predict(X_test)

# SNN accuracy score
snn_accuracy = accuracy_score(y_test, snn_predictions)
print("SNN Accuracy Score: %", snn_accuracy * 100)