import numpy as np
from mytorch.tensor import Tensor
import mytorch.nn as nn

class TinyNN(nn.Module):
	def __init__(self):
		super().__init__()
		self.fc1 = nn.Linear(1, 1)
		self.relu = nn.ReLU()
		self.fc2 = nn.Linear(1, 1)

	def forward(self, x):
		x = self.fc1(x)
		x = self.relu(x)
		x = self.fc2(x)
		x = self.relu(x)    # Reuse relu layer since no params
		return x

model = TinyNN()
for param in model.parameters():
	print(param.data)
 
input = Tensor(np.array([1.0, 2.0]))
output = model(input)
print(output.data)