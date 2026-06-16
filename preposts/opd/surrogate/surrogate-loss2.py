import torch, numpy as np, matplotlib.pyplot as plt

# 设定
pi_ref = torch.tensor([0.1, 0.3, 0.6])
rewards = torch.tensor([10.0, 5.0, 0.0])
beta = 2.0

# 闭式最优解: p*(i) ∝ π_ref(i)·exp(r(i)/β)
log_p_star = torch.log(pi_ref) + rewards / beta
theta_star = (log_p_star - log_p_star[2])[:2]  # θ* = (3.21, 1.81)

# 训练
theta = torch.zeros(2, requires_grad=True)
optimizer = torch.optim.SGD([theta], lr=0.05)
trajectory, J_history = [], []

for step in range(5000):
    logits = torch.cat([theta, torch.zeros(1)])
    p = torch.softmax(logits, dim=0)
    
    # 记录
    with torch.no_grad():
        kl = (p * torch.log(p / pi_ref)).sum()
        J_history.append((p @ rewards - beta * kl).item())
        trajectory.append(theta.detach().clone().numpy())
    
    # 采样
    action = torch.multinomial(p.detach(), 1).item()
    
    # Loss = -J₁^surr - J₂ = -log π_θ(ȳ)·r(ȳ) + β·KL(π_θ||π_ref)
    log_prob = torch.log_softmax(logits, dim=0)[action]
    kl = (p * torch.log(p / pi_ref)).sum()
    loss = -log_prob * rewards[action].detach() + beta * kl
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

trajectory = np.array(trajectory)

# 可视化
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 左: 等高线 + 轨迹
t1 = np.linspace(-2, 5, 200)
t2 = np.linspace(-2, 4, 200)
T1, T2 = np.meshgrid(t1, t2)
Z = np.zeros_like(T1)
for i in range(200):
    for j in range(200):
        logits = np.array([T1[i,j], T2[i,j], 0.0])
        p = np.exp(logits - logits.max()); p /= p.sum()
        Z[i,j] = p @ rewards.numpy() - beta * (p * np.log(p / pi_ref.numpy())).sum()

ax1.contourf(T1, T2, Z, levels=40, cmap='RdYlGn', alpha=0.7)
ax1.contour(T1, T2, Z, levels=20, colors='gray', alpha=0.3, linewidths=0.5)
colors = plt.cm.cool(np.linspace(0, 1, len(trajectory)))
for i in range(len(trajectory)-1):
    ax1.plot(trajectory[i:i+2, 0], trajectory[i:i+2, 1], color=colors[i], lw=0.8, alpha=0.7)
ax1.plot(*trajectory[0], 's', color='blue', ms=10, zorder=10, label='start')
ax1.plot(*trajectory[-1], 'D', color='red', ms=10, zorder=10, label=f'end ({trajectory[-1,0]:.2f}, {trajectory[-1,1]:.2f})')
ax1.plot(*theta_star.numpy(), '*', color='gold', ms=18, markeredgecolor='k', zorder=10,
         label=f'optimal ({theta_star[0]:.2f}, {theta_star[1]:.2f})')
ax1.set(xlabel=r'$\theta_1$', ylabel=r'$\theta_2$', title='REINFORCE trajectory')
ax1.legend(fontsize=9)

# 右: J 曲线
ax2.plot(J_history, alpha=0.4, color='steelblue')
w = 20
ax2.plot(range(w-1, len(J_history)), np.convolve(J_history, np.ones(w)/w, 'valid'),
         color='darkblue', lw=2, label='moving avg')
ax2.axhline(y=J_history[-1], color='gold', ls='--', label=f'$J^*$={max(J_history):.2f}')
ax2.set(xlabel='step', ylabel='$J(\\theta)$', title='$J(\\theta)$ during training')
ax2.legend(); ax2.grid(alpha=0.3)

plt.tight_layout()
# plt.savefig('/mnt/user-data/outputs/reinforce_torch.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"θ* = ({theta_star[0]:.2f}, {theta_star[1]:.2f})")
print(f"θ_final = ({trajectory[-1,0]:.2f}, {trajectory[-1,1]:.2f})")