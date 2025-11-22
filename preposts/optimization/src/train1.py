import torch
import torch.nn as nn
from model1 import SimpleNN
# from plot import graph2d

def train_optimizer():
    # Singleton training data
    X_data = torch.tensor([[2.0]], dtype=torch.float32) # Input x=2
    Y_target = torch.tensor([[1.0]], dtype=torch.float32) # Target y=1

    # Initialize Model, Loss, and Optimizer ---
    model = SimpleNN()
    model.linear.weight.data.fill_(5.0) # w = 5.0 initially
    model.linear.bias.data.fill_(-2.0)  # b = -2.0 initially
    
    criterion = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    
    num_epochs = 100
        
    # Training Loop
    for epoch in range(num_epochs):
        # A. Zero the gradients
        optimizer.zero_grad()
        
        # B. Forward pass
        y_predicted = model(X_data)
        
        # C. Calculate Loss
        loss = criterion(y_predicted, Y_target)
        
        # D. Backward pass (calculates gradients dL/dW and dL/dB)
        loss.backward()
        
        # E. Update parameters
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            w = model.linear.weight.data.item()
            b = model.linear.bias.data.item()
            
            print(f"Epoch [{epoch+1}/{num_epochs}], \t (w, b) = ({w:.4f}, {b:.4f}), \t Loss: {loss.item():.6f}")
                

if __name__ == "__main__":
    train_optimizer()