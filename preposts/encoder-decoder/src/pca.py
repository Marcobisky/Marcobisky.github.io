import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

torch.manual_seed(0)

# ----------------------------
# 1 生成二维高斯数据
# ----------------------------

N = 2000

# 非各向同性 covariance
cov = torch.tensor([[3.0, 0.0],
                    [0.0, 0.2]])

L = torch.linalg.cholesky(cov)
X = torch.randn(N,2) @ L.T


# ----------------------------
# 2 旋转数据
# ----------------------------

theta = np.deg2rad(35)

R = torch.tensor([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
], dtype=torch.float32)

X = X @ R.T


# ----------------------------
# 3 定义 2→1→2 无bias网络
# ----------------------------

class LinearAE(nn.Module):

    def __init__(self):
        super().__init__()

        self.encoder = nn.Linear(2,1,bias=False)
        self.decoder = nn.Linear(1,2,bias=False)

    def forward(self,x):

        z = self.encoder(x)
        x_hat = self.decoder(z)

        return x_hat


model = LinearAE()

optimizer = optim.Adam(model.parameters(), lr=0.05)
loss_fn = nn.MSELoss()


# ----------------------------
# 4 训练
# ----------------------------

for epoch in range(3000):

    x_hat = model(X)

    loss = loss_fn(x_hat,X)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 500 == 0:
        print(epoch, loss.item())


# ----------------------------
# 5 取出 A 和 B
# ----------------------------

A = model.encoder.weight.data      # 1x2
B = model.decoder.weight.data      # 2x1

print("\nA:")
print(A)

print("\nB:")
print(B)

print("\nA^T:")
print(A.T)

print("\nB ≈ A^T ?")


# ----------------------------
# 6 PCA 主方向
# ----------------------------

X_centered = X - X.mean(dim=0)

cov = (X_centered.T @ X_centered) / N

eigvals,eigvecs = torch.linalg.eigh(cov)

principal = eigvecs[:,-1]   # 第一主方向


# ----------------------------
# 7 可视化
# ----------------------------

with torch.no_grad():

    X_hat = model(X)

X_np = X.numpy()
Xhat_np = X_hat.numpy()

plt.figure(figsize=(8,8))

plt.scatter(X_np[:,0],X_np[:,1],
            s=10,alpha=0.3,label="data")

plt.scatter(Xhat_np[:,0],Xhat_np[:,1],
            s=10,alpha=0.3,label="reconstruction")


# PCA direction
scale = 5

origin = np.zeros(2)

p = principal.numpy()

plt.plot(
    [origin[0], p[0]*scale],
    [origin[1], p[1]*scale],
    linewidth=1.5,
    label="PCA direction"
)

# learned subspace

a = A.numpy()[0]

plt.plot(
    [0, a[0]*scale],
    [0, a[1]*scale],
    linewidth=3,
    label="encoder direction"
)

plt.legend()
plt.axis("equal")
plt.title("Linear Autoencoder vs PCA")
plt.show()