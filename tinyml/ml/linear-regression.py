import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. 生成一些线性数据
np.random.seed(0)
X = np.linspace(0, 10, 50)
true_w, true_b = 2.0, 1.0
Y = true_w * X + true_b + np.random.randn(*X.shape)  # 添加高斯噪声

# 2. 初始化参数
w, b = 0.0, 0.0
lr = 0.01
batch_size = 1

# 3. 记录训练过程中的 w, b
params_history = []

# 4. 训练若干轮，记录每次更新后参数
for epoch in range(5):  # 多轮 epoch
    indices = np.random.permutation(len(X))  # 打乱顺序
    for i in range(0, len(X), batch_size):
        idx = indices[i:i+batch_size]
        x_batch = X[idx]
        y_batch = Y[idx]

        # 前向
        y_pred = w * x_batch + b
        loss = np.mean((y_pred - y_batch) ** 2)

        # 梯度
        dw = np.mean(2 * (y_pred - y_batch) * x_batch)
        db = np.mean(2 * (y_pred - y_batch))

        # 更新
        w -= lr * dw
        b -= lr * db

        # 记录
        params_history.append((w, b))

# 5. 动画绘制
fig, ax = plt.subplots()
ax.scatter(X, Y, label="Data")
line, = ax.plot(X, w * X + b, 'r-', label="Prediction")
ax.set_ylim(min(Y)-1, max(Y)+1)
ax.set_title("Linear Regression Training Animation")
ax.legend()

def update(frame):
    w, b = params_history[frame]
    line.set_ydata(w * X + b)
    ax.set_title(f"Step {frame+1}: w={w:.2f}, b={b:.2f}")
    return line,

ani = FuncAnimation(fig, update, frames=len(params_history), interval=100, blit=True)
plt.show()