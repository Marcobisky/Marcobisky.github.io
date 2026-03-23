import numpy as np
from mytorch.tensor import Tensor
import mytorch.nn as nn

data_pt = [(1,3), (2,5), (3,7), (4,9),]

class LinearRegression(nn.Module):
	def __init__(self):
		super().__init__()
		self.fc = nn.Linear(1, 1)

	def forward(self, x):
		x = self.fc(x)
		return x

def _get_batch(data_pt, batch_size=2):
	


def train():
	model = LinearRegression()
	optim = nn.SGD(model.parameters(), lr=0.01)
	criterion = nn.MSELoss()
 
	for epoch in range(200):
		