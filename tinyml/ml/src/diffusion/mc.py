import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

def plot_markov_vector_field(ax, matrix, title):
    # 1. 在单纯形上生成均匀网格点
    grid_res = 15
    x = np.linspace(0, 1, grid_res)
    y = np.linspace(0, 1, grid_res)
    X, Y = np.meshgrid(x, y)
    
    # 过滤出满足 x + y <= 1 的点 (在单纯形内)
    valid = (X + Y) <= 1.0 + 1e-8
    X = X[valid]
    Y = Y[valid]
    Z = 1.0 - X - Y
    
    # 构造状态向量 (每列是一个状态)
    points = np.vstack([X, Y, Z])
    
    # 2. 计算一步转移后的目标点
    # 注意：这里我们统一使用左随机矩阵，状态更新为 v_{t+1} = M * v_t
    next_points = matrix @ points
    
    # 计算位移向量 (即向量场)
    U = next_points[0, :] - X
    V = next_points[1, :] - Y
    W = next_points[2, :] - Z
    
    # 3. 计算模长并归一化方向向量 (确保箭头长度一致)
    magnitudes = np.sqrt(U**2 + V**2 + W**2)
    non_zero = magnitudes > 1e-8
    
    U_norm, V_norm, W_norm = np.zeros_like(U), np.zeros_like(V), np.zeros_like(W)
    U_norm[non_zero] = U[non_zero] / magnitudes[non_zero]
    V_norm[non_zero] = V[non_zero] / magnitudes[non_zero]
    W_norm[non_zero] = W[non_zero] / magnitudes[non_zero]
    
    # 4. 根据模长映射颜色 (蓝小红大: coolwarm)
    norm = plt.Normalize(magnitudes.min(), magnitudes.max())
    colors = cm.coolwarm(norm(magnitudes))
    
    # 5. 绘制单纯形边界
    corners = np.array([[1,0,0], [0,1,0], [0,0,1], [1,0,0]])
    ax.plot(corners[:,0], corners[:,1], corners[:,2], 'k-', alpha=0.3, linewidth=1)
    
    # 6. 绘制向量场 (统一长度，颜色代表大小)
    ax.quiver(X, Y, Z, U_norm, V_norm, W_norm, 
              colors=colors, length=0.06, normalize=False, 
              arrow_length_ratio=0.4, alpha=0.8)
    
    # 7. 绘制两条样本轨迹
    np.random.seed(42)
    for _ in range(2):
        # 生成随机初始分布
        v = np.random.dirichlet((1, 1, 1))
        traj = [v]
        for _ in range(12): # 走 12 步
            v = matrix @ v
            traj.append(v)
        traj = np.array(traj)
        
        # 轨迹线和点
        ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], '-', color='dimgray', linewidth=2, zorder=4)
        ax.scatter(traj[:, 0], traj[:, 1], traj[:, 2], s=30, color='gold', edgecolor='k', zorder=5)
        # 标记起点
        ax.scatter(traj[0, 0], traj[0, 1], traj[0, 2], s=80, marker='X', color='black', zorder=6)

    # 图表设置
    ax.set_title(title, pad=20)
    ax.set_xlabel('State 1')
    ax.set_ylabel('State 2')
    ax.set_zlabel('State 3')
    ax.view_init(elev=35, azim=45)
    
    # 隐藏坐标轴的刻度以保持整洁
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

# ==========================================
# 定义两个矩阵 (均为左随机矩阵，列和为 1)
# ==========================================

# 1. Irreducible MC (不可约，全正矩阵)
P_irreducible = np.array([
    [0.4, 0.3, 0.2],
    [0.4, 0.4, 0.3],
    [0.2, 0.3, 0.5]
])

# 2. Reducible MC (用户提供的矩阵)
P_reducible = np.array([
    [0.4, 0, 0],
    [0.3, 1, 0],
    [0.3, 0, 1]
])

# ==========================================
# 创建画布并绘图
# ==========================================
fig = plt.figure(figsize=(16, 8))

# 子图 1: Irreducible
ax1 = fig.add_subplot(121, projection='3d')
plot_markov_vector_field(ax1, P_irreducible, "Irreducible MC\n(Converges to a Single Point)")

# 子图 2: Reducible
ax2 = fig.add_subplot(122, projection='3d')
plot_markov_vector_field(ax2, P_reducible, "Reducible MC\n(Converges to a Line of Absorbing States)")

plt.tight_layout()
plt.show()