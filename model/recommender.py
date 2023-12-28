import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Load the processed data
X_train = pd.read_csv('/Users/anthonandersson/software/medictionary/data/processed_data/X_train.csv')
y_train = pd.read_csv('/Users/anthonandersson/software/medictionary/data/processed_data/y_train.csv')

# Check the loaded data
print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)

# Ensure that the data is not empty
if X_train.empty or y_train.empty:
    print("Error: Empty data. Check your CSV files.")
    exit()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Check the shapes after splitting
print("X_train shape after split:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape after split:", y_train.shape)
print("y_test shape:", y_test.shape)

# Define the neural network model
class MedicationRecommendationNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(MedicationRecommendationNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Instantiate the model
input_dim = X_train.shape[1]
hidden_dim = 64
output_dim = len(y_train['Medication'].unique())  # Adjust based on your classes
model = MedicationRecommendationNN(input_dim, hidden_dim, output_dim)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Convert your data to PyTorch tensors
X_train_tensor = torch.Tensor(X_train.values)
y_train_tensor = torch.LongTensor(LabelEncoder().fit_transform(y_train['Medication']))

# Train the model
epochs = 10
for epoch in range(epochs):
    # Forward pass
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)

    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Print training loss
    print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item()}')

# Evaluate the model on the test set
with torch.no_grad():
    X_test_tensor = torch.Tensor(X_test.values)
    predictions = model(X_test_tensor)
    _, predicted_classes = torch.max(predictions, 1)

# Convert predicted classes back to medication names
predicted_medication = LabelEncoder().inverse_transform(predicted_classes.numpy())

# Save the trained model
torch.save(model.state_dict(), 'models/medication_recommendation_model.pth')

# Print the predicted medications for the test set
print("Predicted Medications:")
print(predicted_medication)