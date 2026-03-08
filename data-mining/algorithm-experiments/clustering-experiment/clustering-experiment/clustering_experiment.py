import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

data = pd.read_excel("sample_dataset_01.xlsx", sheet_name="Clear_Data")

print(data.head())

X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(X_scaled)

kmeans_labels = kmeans.labels_

print("K-Means Cluster Centers:\n", kmeans.cluster_centers_)
print("K-Means Labels:\n", kmeans_labels)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.1, random_state=42)

snn_model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
snn_model.fit(X_train, y_train)

snn_predictions = snn_model.predict(X_test)

snn_accuracy = accuracy_score(y_test, snn_predictions)
print("SNN Accuracy Score:", f"%{snn_accuracy*100}")