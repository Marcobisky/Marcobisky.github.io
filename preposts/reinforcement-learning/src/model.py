import torch
import torch.nn as nn
import torch.optim as optim

# 2. Policy Network
class Position2Prob(nn.Module):
    def __init__(self):
        super(Position2Prob, self).__init__()
        self.fc1 = nn.Linear(2, 16)
        self.fc2 = nn.Linear(16, 3)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.softmax(self.fc2(x), dim=-1)
        return x