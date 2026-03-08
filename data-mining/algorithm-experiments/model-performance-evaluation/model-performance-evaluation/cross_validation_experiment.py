import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold

class SimpleNeuralNetwork:
    def __init__(self, input_size):
        np.random.seed(42)  # Fixed seed for randomness control
        self.weights = np.random.randn(input_size)
        self.bias = np.random.randn()
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def sigmoid_derivative(self, z):
        return z * (1 - z)
    
    def predict(self, X):
        z = np.dot(X, self.weights) + self.bias
        return self.sigmoid(z)
    
    def train(self, X, y, epochs=1000, lr=0.001):  # More appropriate learning rate and epoch number
        losses = []
        for epoch in range(epochs):
            epoch_loss = 0
            for i in range(len(X)):
                xi = X[i]
                target = y[i]
                
                z = np.dot(xi, self.weights) + self.bias
                output = self.sigmoid(z)
                
                error = target - output
                epoch_loss += error ** 2  # MSE loss
                
                adjustment = error * self.sigmoid_derivative(output)
                
                # Update weights and bias
                self.weights += lr * adjustment * xi
                self.bias += lr * adjustment
            losses.append(epoch_loss / len(X))
            if epoch % 100 == 0:
                print(f"Epoch {epoch}: Loss: {losses[-1]}")
        return losses

class KMeans:
    def __init__(self, k=2, max_iters=100):
        self.k = k
        self.max_iters = max_iters
    
    def fit(self, X):
        self.centroids = X[np.random.choice(len(X), self.k, replace=False)]
        
        for _ in range(self.max_iters):
            self.labels = self._assign_clusters(X)
            new_centroids = self._update_centroids(X)
            
            if np.all(self.centroids == new_centroids):
                break
            
            self.centroids = new_centroids
    
    def _assign_clusters(self, X):
        distances = np.array([np.linalg.norm(X - centroid, axis=1) for centroid in self.centroids])
        return np.argmin(distances, axis=0)
    
    def _update_centroids(self, X):
        return np.array([X[self.labels == i].mean(axis=0) for i in range(self.k)])
    
    def predict(self, X):
        return self._assign_clusters(X)

def load_data(filepath, sheet_name='2D-Dataset'):
    df = pd.read_excel(filepath, sheet_name=sheet_name)
    y = df['age'][1:].values
    X = df['education_level'][1:].values
    y = pd.factorize(y)[0]
    X = pd.factorize(X)[0]
    return X.reshape(-1, 1), y

if __name__ == "__main__":
    # Load dataset
    X, y = load_data('simple_dataset.xlsx')
    
    # Standardize data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Cross-validation settings
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    kmeans_accuracies = []
    snn_accuracies = []
    
    for train_index, test_index in kf.split(X_scaled):
        X_train, X_test = X_scaled[train_index], X_scaled[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        # K-means Model
        kmeans = KMeans(k=2, max_iters=250)
        kmeans.fit(X_train)
        kmeans_predictions = kmeans.predict(X_test)
        if np.isnan(kmeans.centroids).any():
            print("Warning: Empty clusters detected in K-means algorithm.")
        correct_labels = (kmeans_predictions == y_test) | (kmeans_predictions == (1 - y_test))
        kmeans_accuracy = np.mean(correct_labels)
        kmeans_accuracies.append(kmeans_accuracy)
        print(f"K-means Fold Accuracy: %{kmeans_accuracy * 100}")
        
        # Simple Neural Network Model
        snn = SimpleNeuralNetwork(input_size=1)
        snn.train(X_train, y_train, epochs=1000, lr=0.001)
        snn_predictions = snn.predict(X_test) > 0.5
        snn_accuracy = np.mean(snn_predictions == y_test)
        snn_accuracies.append(snn_accuracy)
        print(f"SNN Fold Accuracy: %{snn_accuracy * 100}")

    print(f"K-means Mean Accuracy: %{np.mean(kmeans_accuracies) * 100}")
    print(f"SNN Mean Accuracy: %{np.mean(snn_accuracies) * 100}")

    # Visualize the data
    plt.scatter(X_scaled, y, c=y, cmap='coolwarm')
    plt.xlabel('Education Level (scaled)')
    plt.ylabel('Age')
    plt.title('2D Dataset')
    plt.show()