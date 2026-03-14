import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm

# ==========================================
# 1. 准备向量场数据
# ==========================================
grid_res = 20
a_vals = np.linspace(0, 1, grid_res)
b_vals = np.linspace(0, 1, grid_res)
A, B = np.meshgrid(a_vals, b_vals)

# 计算位移向量 (Delta a, Delta b)
# a_{t+1} = (1 - b_t)/2  =>  U = (1 - B)/2 - A
# b_{t+1} = (1 - a_t)/2  =>  V = (1 - A)/2 - B
U = (1 - B) / 2 - A
V = (1 - A) / 2 - B

# 计算模长并归一化
magnitudes = np.sqrt(U**2 + V**2)
U_norm = np.zeros_like(U)
V_norm = np.zeros_like(V)
non_zero = magnitudes > 1e-8
U_norm[non_zero] = U[non_zero] / magnitudes[non_zero]
V_norm[non_zero] = V[non_zero] / magnitudes[non_zero]

# 颜色映射 (红色模长大，蓝色模长小)
norm = plt.Normalize(magnitudes.min(), magnitudes.max())
colors = cm.coolwarm(norm(magnitudes))

# ==========================================
# 2. 准备样本轨迹数据
# ==========================================
# 选取两个初始点 (a, b)
initial_points = np.array([[0.1, 0.95]])
steps = 15
trajectories = np.zeros((len(initial_points), steps, 2))

for i, pt in enumerate(initial_points):
    trajectories[i, 0] = pt
    for t in range(1, steps):
        curr_a, curr_b = trajectories[i, t-1]
        next_a = (1 - curr_b) / 2
        next_b = (1 - curr_a) / 2
        trajectories[i, t] = [next_a, next_b]

# ==========================================
# 3. 设置画布和子图
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Jacobi Update", fontsize=16)

# --- 子图 1: 2D 向量场 ---
ax1.set_title("Vector Field")
ax1.set_xlabel("a (Distance from left)")
ax1.set_ylabel("b (Distance from right)")
ax1.set_xlim(-0.05, 1.05)
ax1.set_ylim(-0.05, 1.05)
ax1.set_aspect('equal')
ax1.grid(True, linestyle='--', alpha=0.5)

# 画向量场
ax1.quiver(A, B, U_norm, V_norm, color=colors.reshape(-1, 4), 
           scale=25, headwidth=4, headlength=5, alpha=0.6)

# 标记收敛中心 (1/3, 1/3)
ax1.scatter([1/3], [1/3], color='red', marker='*', s=200, zorder=5, label='Fixed Point (1/3, 1/3)')
ax1.legend()

# 轨迹线和当前点的占位符
lines = [ax1.plot([], [], '-', lw=2, color='dimgray')[0] for _ in range(len(initial_points))]
points = [ax1.plot([], [], 'o', markersize=8, markeredgecolor='k')[0] for _ in range(len(initial_points))]

# --- 子图 2: 1D 单位线段 ---
ax2.set_title("Visualized on Line Segment")
ax2.set_xlim(-0.1, 1.1)
ax2.set_ylim(-0.5, 0.5)
ax2.get_xaxis().set_visible(False)
ax2.get_yaxis().set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)

# 画底部的线段 (0 到 1)
ax2.plot([0, 1], [0, 0], 'k-', lw=4)
ax2.plot([0, 1], [0, 0], 'k|', markersize=20)
ax2.text(0, -0.1, "0", ha='center', fontsize=12)
ax2.text(1, -0.1, "1", ha='center', fontsize=12)

# # 标记理想的三等分点
# ax2.plot([1/3, 2/3], [0, 0], 'x', color='gray', markersize=10)
# ax2.text(1/3, 0.08, "1/3", ha='center', color='gray')
# ax2.text(2/3, 0.08, "2/3", ha='center', color='gray')

# 我们只展示第一条轨迹 (从 a=0, b=0 开始) 在线段上的变化
pt_a, = ax2.plot([], [], 'ro', markersize=12, label='Point a (from left)')
pt_b, = ax2.plot([], [], 'bo', markersize=12, label='Point b (from right)')
text_a = ax2.text(0, 0.15, "", ha='center', color='red', fontsize=11)
text_b = ax2.text(0, 0.15, "", ha='center', color='blue', fontsize=11)
ax2.legend(loc='upper right')

# ==========================================
# 4. 动画更新函数
# ==========================================
def init():
    for line in lines:
        line.set_data([], [])
    for point in points:
        point.set_data([], [])
    pt_a.set_data([], [])
    pt_b.set_data([], [])
    text_a.set_text("")
    text_b.set_text("")
    return lines + points + [pt_a, pt_b, text_a, text_b]

def update(frame):
    # 更新 2D 轨迹
    for i, traj in enumerate(trajectories):
        x_data = traj[:frame+1, 0]
        y_data = traj[:frame+1, 1]
        lines[i].set_data(x_data, y_data)
        points[i].set_data([x_data[-1]], [y_data[-1]])
        # 给当前点上色区分
        points[i].set_color('orange' if i==0 else 'cyan')
        
    # 更新 1D 线段 (取第一条轨迹 trajectory[0])
    current_a = trajectories[0, frame, 0]
    current_b = trajectories[0, frame, 1]
    
    # 坐标位置：a 是从左往右 (坐标为 a)，b 是从右往左 (坐标为 1-b)
    coord_a = current_a
    coord_b = 1 - current_b
    
    pt_a.set_data([coord_a], [0])
    pt_b.set_data([coord_b], [0])
    
    text_a.set_position((coord_a, 0.12))
    text_a.set_text(f"a={current_a:.3f}")
    
    text_b.set_position((coord_b, -0.18))
    text_b.set_text(f"b={current_b:.3f}")
    
    return lines + points + [pt_a, pt_b, text_a, text_b]

# 创建动画 (间隔 800ms，共 15 帧)
ani = animation.FuncAnimation(fig, update, frames=steps, init_func=init, 
                              interval=500, blit=True, repeat_delay=2000)

plt.tight_layout()
plt.show()

# ani.save('find-point-sync.gif', writer='pillow', fps=2)