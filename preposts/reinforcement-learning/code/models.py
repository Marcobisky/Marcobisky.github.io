import torch
import torch.nn as nn

# Neural network model
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(9, 64),
            nn.ReLU(),
            nn.Linear(64, 9)
        )
    def forward(self, x):
        return self.fc(x)