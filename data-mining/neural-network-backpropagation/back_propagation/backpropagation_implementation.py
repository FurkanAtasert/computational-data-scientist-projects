import numpy as np
import matplotlib.pyplot as plt
import pandas as pd  
from scipy import stats


# Load the dataset
data = pd.read_excel("sample_data.xlsx")

# ReLU activation function
def relu(x):
    return np.maximum(0, x)

# Derivative of the ReLU function
def relu_derivative(x):
    return np.where(x <= 0, 0, 1)

# Artificial Neural Network class
class NeuralNetwork:
    def __init__(self, layers):
        # List of neural network layers
        self.layers = layers
        # Initialize weights randomly
        self.weights = [np.random.randn(layers[i], layers[i+1]) * np.sqrt(2 / layers[i]) for i in range(len(layers) - 1)]
        # Initialize biases randomly
        self.biases = [np.zeros((1, layers[i+1])) for i in range(len(layers) - 1)]
    
    # Forward propagation function
    def forward(self, x):
        # Lists for Z values and activation values
        self.z_values = []
        self.activation_values = [x]
        for i in range(len(self.weights)):
            # Calculate activation output
            z = np.dot(self.activation_values[-1], self.weights[i]) + self.biases[i]
            self.z_values.append(z)
            activation = relu(z)
            self.activation_values.append(activation)
        return self.activation_values[-1]
    
    # Backpropagation function
    def backward(self, y):
        # Calculate error
        self.error = y - self.activation_values[-1]
        # Compute delta values
        self.delta = [self.error]
        for i in range(len(self.z_values) - 1, 0, -1):
            error = np.dot(self.delta[-1], self.weights[i].T)
            delta = error * relu_derivative(self.activation_values[i])
            self.delta.append(delta)
        self.delta.reverse()
        
        # Compute gradients
        self.gradient_weights = []
        self.gradient_biases = []
        for i in range(len(self.weights)):
            gradient_weight = np.dot(self.activation_values[i].T, self.delta[i])
            gradient_bias = np.sum(self.delta[i], axis=0)
            self.gradient_weights.append(gradient_weight)
            self.gradient_biases.append(gradient_bias)
        
    # Update weights and biases
    def update_weights(self, learning_rate):
        for i in range(len(self.weights)):
            self.weights[i] += learning_rate * self.gradient_weights[i]
            self.biases[i] += learning_rate * self.gradient_biases[i]
    
    # Train the model
    def fit(self, X_train, y_train, epochs, learning_rate):
        self.loss = []
        for epoch in range(epochs):
            # Forward pass, backpropagation, and update
            self.forward(X_train)
            self.backward(y_train)
            self.update_weights(learning_rate)
            # Compute loss
            loss = np.mean(np.square(self.error))
            self.loss.append(loss)
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss}")
        print("Training completed.")
    
        
    # Make predictions on test data
    def predict(self, X_test):
        return self.forward(X_test)

# Load dataset and separate inputs and targets
X = data.drop(columns=["tumor-size"]).values
y = data["tumor-size"].values.reshape(-1, 1)

# Create and train the model (HIDDEN LAYERS)
# The number of epochs can be increased, but to avoid overfitting it was set to 1000.
# The learning rate was kept lower to improve the learning process.
# Since there are 15004 data samples, training was chosen to be performed 1000 times.
nn = NeuralNetwork([X.shape[1], 2, 16, 8, 1])
nn.fit(X, y, epochs=400, learning_rate=0.00000001)

# Make predictions
predictions = nn.predict(X)
rounded_predictions = np.round(predictions)

# Display predicted values
print("Predicted Values:")
for i in range(len(X)):
    print(f"Input: {X[i]}, True Value: {y[i]}, Prediction: {rounded_predictions[i]}")
    
# Calculate accuracy
accuracy = np.mean(rounded_predictions == y)
print(f"The model achieved {accuracy*100:.2f}% accuracy in predicting the target values based on the training dataset. The higher this rate, the better the model performs on the data.\nDeveloper Name: Furkan Atasert")

# Calculate residuals
residuals = y - predictions
print("Residuals Shape:", residuals.shape)
residuals = residuals.flatten()


# Plot loss values
plt.figure(figsize=(10, 5))
plt.plot(nn.loss)
plt.title("Loss Value Change")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.grid(True)
plt.text(0.5, 0.95, "Change of loss values during the training process", ha='center', va='center', transform=plt.gca().transAxes)
plt.show()

# Residuals histogram
plt.figure(figsize=(10, 5))
plt.hist(residuals, bins=30, edgecolor='k', alpha=0.7)
plt.title("Frequency Histogram of Model Errors")
plt.xlabel("Error Value")
plt.ylabel("Frequency")
plt.grid(True)
plt.text(0.5, 0.95, "Histogram of error frequencies based on training data", ha='center', va='center', transform=plt.gca().transAxes)
plt.show()

# Q-Q plot
plt.figure(figsize=(10, 5))
stats.probplot(residuals, dist="norm", plot=plt)
plt.title("Q-Q Plot")
plt.xlabel("Theoretical Normal Values")
plt.ylabel("Ordered Residuals")
plt.grid(True)
plt.text(0.5, 0.95, "Fit of model predictions to actual data", ha='center', va='center', transform=plt.gca().transAxes)
plt.show()