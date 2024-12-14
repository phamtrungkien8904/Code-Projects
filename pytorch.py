import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# Data
x_train = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0], [7.0], [8.0], [9.0], [10.0]], dtype=torch.float32)
y_train = torch.tensor([[149.7], [301.2], [449.7], [601.8], [752.0], [898.0], [1052.2], [1200.2], [1351.0], [1500.0]], dtype=torch.float32)

# Model
class LinearRegressionModel(nn.Module):
    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        self.linear = nn.Linear(1, 1)
    def forward(self, x):
        return self.linear(x)

model = LinearRegressionModel()

# Loss and optimizer
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# Training loop
num_epochs = 100
for epoch in range(num_epochs):
    y_pred = model(x_train)
    loss = criterion(y_pred, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# Test the model
with torch.no_grad():
    x_test = torch.tensor([[6.0], [7.0]], dtype=torch.float32)
    y_test_pred = model(x_test)
    print(f'Predicted prices for houses of size 6k and 7k sq ft: {y_test_pred.numpy()}')

# Plot the results
with torch.no_grad():
    predicted = model(x_train).detach().numpy()
    plt.scatter(x_train.numpy(), y_train.numpy(), label='Original Data', color='blue')
    plt.plot(x_train.numpy(), predicted, label='Fitted Line', color='red')
    plt.xlabel('House Size (1000 sq ft)')
    plt.ylabel('House Price ($1000)')
    plt.legend()
    plt.show()
