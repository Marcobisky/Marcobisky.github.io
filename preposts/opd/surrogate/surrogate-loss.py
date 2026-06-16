import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ============================================================
# 设定
# ============================================================
pi_ref = np.array([0.1, 0.3, 0.6])   # 参考策略: A=0.1, B=0.3, C=0.6
rewards = np.array([10.0, 5.0, 0.0])  # 奖励:     A=10,  B=5,   C=0
beta = 2.0                             # KL 惩罚系数
lr = 0.05                              # 学习率
n_steps = 10000                          # 训练步数
np.random.seed(42)

# ============================================================
# 工具函数
# ============================================================
def softmax(theta1, theta2):
    """(θ₁, θ₂) → (p_A, p_B, p_C)，第三个 logit 固定为 0"""
    logits = np.array([theta1, theta2, 0.0])
    logits -= logits.max()  # 数值稳定
    e = np.exp(logits)
    return e / e.sum()

def kl_divergence(p, q):
    """KL(p || q)，用于计算 KL(π_θ || π_ref)"""
    return np.sum(p * np.log(p / q))

def J_exact(theta1, theta2):
    """精确计算 J(θ) = E[r] - β·KL(π_θ || π_ref)，用于画等高线"""
    p = softmax(theta1, theta2)
    return p @ rewards - beta * kl_divergence(p, pi_ref)

# ============================================================
# 最优解（闭式）: p*(i) ∝ π_ref(i) · exp(r(i)/β)
# ============================================================
log_p_star = np.log(pi_ref) + rewards / beta
log_p_star -= log_p_star.max()
p_star = np.exp(log_p_star)
p_star /= p_star.sum()
# softmax(θ₁*, θ₂*, 0) = p*  →  θᵢ* = log(p*(i)/p*(C))
theta1_star = np.log(p_star[0] / p_star[2])
theta2_star = np.log(p_star[1] / p_star[2])
print(f"最优解: θ₁* = {theta1_star:.3f}, θ₂* = {theta2_star:.3f}")
print(f"最优分布: p*(A)={p_star[0]:.3f}, p*(B)={p_star[1]:.3f}, p*(C)={p_star[2]:.3f}")
print(f"最优 J = {J_exact(theta1_star, theta2_star):.3f}")
print()

# ============================================================
# REINFORCE 训练（单样本 surrogate + 精确 KL 梯度）
# ============================================================
theta1, theta2 = 0.0, 0.0  # 初始: 均匀分布
trajectory = [(theta1, theta2)]
J_history = []

for step in range(n_steps):
    p = softmax(theta1, theta2)
    
    # 记录真实 J 值
    J_val = p @ rewards - beta * kl_divergence(p, pi_ref)
    J_history.append(J_val)
    
    # --- 采样一个 action ---
    action = np.random.choice(3, p=p)  # 0=A, 1=B, 2=C
    r = rewards[action]
    
    # --- J₁ 的 surrogate 梯度 ---
    # J₁^surr = log π_θ(ȳ) · r(ȳ)
    # ∂ log p(action) / ∂θ₁ = 1_{action=A} - p_A
    # ∂ log p(action) / ∂θ₂ = 1_{action=B} - p_B
    # （这是 softmax 的标准导数）
    dlogp_dtheta1 = (1.0 if action == 0 else 0.0) - p[0]
    dlogp_dtheta2 = (1.0 if action == 1 else 0.0) - p[1]
    
    grad_J1_theta1 = dlogp_dtheta1 * r  # ∇θ₁ J₁^surr
    grad_J1_theta2 = dlogp_dtheta2 * r  # ∇θ₂ J₁^surr
    
    # --- J₂ = -β·KL 的精确梯度（直接求导，不需要 surrogate）---
    # KL(π_θ || π_ref) = Σᵢ p(i) log(p(i)/π_ref(i))
    # ∂KL/∂θ₁ = Σᵢ ∂p(i)/∂θ₁ · [log(p(i)/π_ref(i)) + 1]
    #          = Σᵢ ∂p(i)/∂θ₁ · log(p(i)/π_ref(i))   （因为 Σ ∂p/∂θ = 0）
    log_ratio = np.log(p / pi_ref)  # [log(pA/0.1), log(pB/0.3), log(pC/0.6)]
    
    # ∂p(i)/∂θ₁ = p(i)(1_{i=A} - p(A))
    dp_dtheta1 = p * (np.array([1, 0, 0]) - p[0])
    dp_dtheta2 = p * (np.array([0, 1, 0]) - p[1])
    
    dKL_dtheta1 = dp_dtheta1 @ log_ratio
    dKL_dtheta2 = dp_dtheta2 @ log_ratio
    
    grad_J2_theta1 = -beta * dKL_dtheta1
    grad_J2_theta2 = -beta * dKL_dtheta2
    
    # --- 合并梯度，梯度上升 ---
    theta1 += lr * (grad_J1_theta1 + grad_J2_theta1)
    theta2 += lr * (grad_J1_theta2 + grad_J2_theta2)
    
    trajectory.append((theta1, theta2))

trajectory = np.array(trajectory)
print(f"训练结束: θ₁ = {theta1:.3f}, θ₂ = {theta2:.3f}")
print(f"最终 J = {J_history[-1]:.3f}")

# ============================================================
# 可视化
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# --- 左图: θ 轨迹 + J 的等高线 ---
ax = axes[0]

# 等高线网格
t1_range = np.linspace(-2, 5, 200)
t2_range = np.linspace(-2, 4, 200)
T1, T2 = np.meshgrid(t1_range, t2_range)
Z = np.vectorize(J_exact)(T1, T2)

contour = ax.contourf(T1, T2, Z, levels=40, cmap='RdYlGn', alpha=0.7)
ax.contour(T1, T2, Z, levels=20, colors='gray', alpha=0.3, linewidths=0.5)
plt.colorbar(contour, ax=ax, label='$J(\\theta)$', shrink=0.8)

# 训练轨迹: 用颜色编码步数
n = len(trajectory)
colors = plt.cm.cool(np.linspace(0, 1, n))
for i in range(n - 1):
    ax.plot(trajectory[i:i+2, 0], trajectory[i:i+2, 1],
            color=colors[i], linewidth=0.8, alpha=0.7)

# 每隔一些步画点
step_markers = list(range(0, n, 20)) + [n-1]
for i in step_markers:
    ax.plot(trajectory[i, 0], trajectory[i, 1], 'o',
            color=colors[i], markersize=4, zorder=5)

# 起点和终点
ax.plot(trajectory[0, 0], trajectory[0, 1], 's', color='blue',
        markersize=10, zorder=10, label=f'start (0, 0)')
ax.plot(trajectory[-1, 0], trajectory[-1, 1], 'D', color='red',
        markersize=10, zorder=10, label=f'end ({theta1:.2f}, {theta2:.2f})')
ax.plot(theta1_star, theta2_star, '*', color='gold', markersize=18,
        markeredgecolor='black', markeredgewidth=1, zorder=10,
        label=f'optimal ({theta1_star:.2f}, {theta2_star:.2f})')

ax.set_xlabel('$\\theta_1$ (controls $p_A$)', fontsize=12)
ax.set_ylabel('$\\theta_2$ (controls $p_B$)', fontsize=12)
ax.set_title('REINFORCE training trajectory\n'
             '$J(\\theta) = \\mathbb{E}[r(y)] - \\beta \\cdot KL(\\pi_\\theta \\| \\pi_{ref})$',
             fontsize=13)
ax.legend(fontsize=10, loc='upper left')

# --- 右图: J 随训练步数变化 ---
ax2 = axes[1]
ax2.plot(J_history, color='steelblue', linewidth=1, alpha=0.6, label='$J(\\theta)$ per step')

# 滑动平均
window = 20
if len(J_history) >= window:
    J_smooth = np.convolve(J_history, np.ones(window)/window, mode='valid')
    ax2.plot(range(window-1, len(J_history)), J_smooth,
             color='darkblue', linewidth=2, label=f'moving avg (window={window})')

ax2.axhline(y=J_exact(theta1_star, theta2_star), color='gold',
            linestyle='--', linewidth=2, label=f'optimal $J^*$ = {J_exact(theta1_star, theta2_star):.3f}')
ax2.set_xlabel('Training step', fontsize=12)
ax2.set_ylabel('$J(\\theta)$', fontsize=12)
ax2.set_title('$J(\\theta)$ during training', fontsize=13)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
# plt.savefig('./reinforce_training.png', dpi=150, bbox_inches='tight')
plt.show()
# plt.close()
# print("\n图片已保存")