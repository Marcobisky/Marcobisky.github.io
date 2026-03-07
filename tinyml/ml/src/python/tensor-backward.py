import mytorch as torch
import numpy as np

x1 = torch.Tensor(np.array([2]), requires_grad=True)
x2 = torch.Tensor(np.array([5]), requires_grad=True)

v1 = torch.Log().forward(x1)
v2 = x1 * x2
v3 = torch.Exp().forward(x2)

v4 = v1 + v2

loss = v4 - v3
print("loss =", loss.data)

loss.backward()

print("x1.grad =", x1.grad)
print("x2.grad =", x2.grad)