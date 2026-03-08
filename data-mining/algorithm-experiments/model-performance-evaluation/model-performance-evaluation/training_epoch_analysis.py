import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class SimpleNeuralNetwork:
    def __init__(self, input_size):
        self.weights = np.random.randn(input_size)
        self.bias = np.random.randn()
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def sigmoid_derivative(self, z):
        return z * (1 - z)
    
    def predict(self, X):
        z = np.dot(X, self.weights) + self.bias
        return self.sigmoid(z)
    
    def train(self, X, y, epochs=1999, lr=0.01):
        train_errors = []
        best_epoch = 0
        best_error = float('inf')
        last_error = float('inf')
        early_stopping_count = 0
        lr_decay_epoch = epochs // 10
        lr_decay_factor = 0.9
        
        for epoch in range(epochs):
            epoch_errors = []
            
            for i in range(len(X)):
                xi = X[i]
                target = y[i]
                
                z = np.dot(xi, self.weights) + self.bias
                output = self.sigmoid(z)
                
                error = target - output
                epoch_errors.append(error)
                
                adjustment = error * self.sigmoid_derivative(output)
                
                self.weights += lr * adjustment * xi
                self.bias += lr * adjustment
            
            epoch_error = np.mean(np.abs(epoch_errors))
            train_errors.append(epoch_error)
            
            if epoch % 100 == 0:
                print(f"Epoch {epoch}: Error: {epoch_error}")
            
            # Learning rate decay
            if epoch % lr_decay_epoch == 0 and epoch != 0:
                lr *= lr_decay_factor
            
            # Early stopping mechanism
            if epoch_error >= last_error:
                early_stopping_count += 1
            else:
                early_stopping_count = 0
            
            if early_stopping_count == 3:
                print("Early stopping triggered.")
                break
            
            # Update last error
            last_error = epoch_error

            # Update best epoch
            if epoch_error < best_error:
                best_error = epoch_error
                best_epoch = epoch

        print(f"Best epoch: {best_epoch}")
        return train_errors

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

    # Convert categorical variables to numerical values
    y = pd.factorize(y)[0]
    X = pd.factorize(X)[0]
    
    return X.reshape(-1, 1), y

if __name__ == "__main__":
    # Load dataset
    X, y = load_data('simple_dataset.xlsx')

    # Visualize the dataset (since it is categorical, visualization must reflect that)
    plt.scatter(X, y, c=y, cmap='coolwarm')
    plt.xlabel('Education Level')
    plt.ylabel('Age')
    plt.title('2D Dataset')
    plt.show()

    # Simple Neural Network Model
    snn = SimpleNeuralNetwork(input_size=1)
    train_errors = snn.train(X, y, epochs=2000, lr=0.01)
    snn_predictions = snn.predict(X) > 0.5
    snn_accuracy = np.mean(snn_predictions == y)