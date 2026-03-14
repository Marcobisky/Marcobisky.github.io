import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ==========================================
# 1. 准备交替更新的轨迹数据
# ==========================================
steps = 8  # 完整的迭代轮数
initial_a, initial_b = 0.1, 0.95

# 我们将每一步单变量的更新都记录下来，以画出横竖交替的直线
# 初始点: (a0, b0)
# 第1步:  (a0, b1)  -> 只更新 b，竖直线
# 第2步:  (a1, b1)  -> 只更新 a，水平线
trajectories = [[initial_a, initial_b]]

curr_a, curr_b = initial_a, initial_b
for _ in range(steps):
    # 1. 先用当前的 a 更新 b
    curr_b = (1 - curr_a) / 2
    trajectories.append([curr_a, curr_b])
    
    # 2. 再用刚刚得到的新 b 更新 a
    curr_a = (1 - curr_b) / 2
    trajectories.append([curr_a, curr_b])

trajectories = np.array(trajectories)
total_frames = len(trajectories)

# ==========================================
# 2. 设置画布和子图
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Gauss-Seidel Method (Converge Faster)", fontsize=16)

# --- 子图 1: 2D 阶梯轨迹 ---
ax1.set_title("Cobweb Plot")
ax1.set_xlabel("a (Distance from left)")
ax1.set_ylabel("b (Distance from right)")
ax1.set_xlim(-0.05, 1.05)
ax1.set_ylim(-0.05, 1.05)
ax1.set_aspect('equal')
ax1.grid(True, linestyle='--', alpha=0.5)

# 绘制两条约束直线，它们的交点就是不动点
a_vals = np.linspace(-0.1, 1.1, 100)
# 线 1: b = (1-a)/2
ax1.plot(a_vals, (1 - a_vals) / 2, 'b--', alpha=0.5, label='Constraint: b = (1-a)/2')
# 线 2: a = (1-b)/2  =>  b = 1 - 2a
ax1.plot(a_vals, 1 - 2 * a_vals, 'r--', alpha=0.5, label='Constraint: a = (1-b)/2')

# 标记收敛中心 (1/3, 1/3)
ax1.scatter([1/3], [1/3], color='black', marker='*', s=150, zorder=5, label='Fixed Point (1/3, 1/3)')
ax1.legend()

# 轨迹线和当前点
line_2d, = ax1.plot([], [], '-', lw=2, color='darkorange')
point_2d, = ax1.plot([], [], 'o', markersize=8, color='darkred')

# --- 子图 2: 1D 交替移动 ---
ax2.set_title("Visualized on Line Segment")
ax2.set_xlim(-0.1, 1.1)
ax2.set_ylim(-0.5, 0.5)
ax2.get_xaxis().set_visible(False)
ax2.get_yaxis().set_visible(False)
for spine in ['top', 'right', 'left', 'bottom']:
    ax2.spines[spine].set_visible(False)

# 画底部的线段
ax2.plot([0, 1], [0, 0], 'k-', lw=4)
ax2.plot([0, 1], [0, 0], 'k|', markersize=20)
ax2.text(0, -0.1, "0", ha='center', fontsize=12)
ax2.text(1, -0.1, "1", ha='center', fontsize=12)

# # 标记理想的三等分点
# ax2.plot([1/3, 2/3], [0, 0], 'x', color='gray', markersize=10)
# ax2.text(1/3, 0.08, "1/3", ha='center', color='gray')
# ax2.text(2/3, 0.08, "2/3", ha='center', color='gray')

# 在线段上的两个点
pt_a, = ax2.plot([], [], 'ro', markersize=12, label='Point a (updates 2nd)')
pt_b, = ax2.plot([], [], 'bo', markersize=12, label='Point b (updates 1st)')
text_a = ax2.text(0, 0.15, "", ha='center', color='red', fontsize=11)
text_b = ax2.text(0, 0.15, "", ha='center', color='blue', fontsize=11)
ax2.legend(loc='upper right')

# ==========================================
# 3. 动画更新函数
# ==========================================
def init():
    line_2d.set_data([], [])
    point_2d.set_data([], [])
    pt_a.set_data([], [])
    pt_b.set_data([], [])
    text_a.set_text("")
    text_b.set_text("")
    return line_2d, point_2d, pt_a, pt_b, text_a, text_b

def update(frame):
    # 更新 2D 轨迹 (画出到当前帧为止的所有阶梯)
    x_data = trajectories[:frame+1, 0]
    y_data = trajectories[:frame+1, 1]
    line_2d.set_data(x_data, y_data)
    point_2d.set_data([x_data[-1]], [y_data[-1]])
    
    # 更新 1D 线段
    current_a = trajectories[frame, 0]
    current_b = trajectories[frame, 1]
    coord_b = 1 - current_b
    
    pt_a.set_data([current_a], [0])
    pt_b.set_data([coord_b], [0])
    
    text_a.set_position((current_a, 0.12))
    text_a.set_text(f"a={current_a:.3f}")
    
    text_b.set_position((coord_b, -0.18))
    text_b.set_text(f"b={current_b:.3f}")
    
    return line_2d, point_2d, pt_a, pt_b, text_a, text_b

# 创建动画 (间隔 1000ms 方便看清交替过程)
ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, 
                              interval=500, blit=True, repeat_delay=2000)

plt.tight_layout()
plt.show()

# ani.save('find-point-async.gif', writer='pillow', fps=2)