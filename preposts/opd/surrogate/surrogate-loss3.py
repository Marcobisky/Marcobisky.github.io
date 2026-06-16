import torch, numpy as np, matplotlib.pyplot as plt

pi_ref = torch.tensor([0.1, 0.3, 0.6])
# rewards = torch.tensor([100.0, 95.0, 90.0])
# rewards = torch.tensor([10.0, 5.0, 0.0])
rewards = torch.tensor([0.0, -95.0, -100.0])
beta = 2.0
n_steps = 700
lr = 0.05
torch.manual_seed(0)

# 最优解
log_p_star = torch.log(pi_ref) + rewards / beta
theta_star = (log_p_star - log_p_star[2])[:2].numpy()

def train(G, use_baseline=False, seed=0):
    """G 个样本的 REINFORCE；G=None 表示精确梯度（穷举所有 action）"""
    torch.manual_seed(seed)
    theta = torch.zeros(2, requires_grad=True)
    opt = torch.optim.SGD([theta], lr=lr)
    traj, Js = [], []

    for _ in range(n_steps):
        logits = torch.cat([theta, torch.zeros(1)])
        p = torch.softmax(logits, dim=0)
        log_p = torch.log_softmax(logits, dim=0)

        with torch.no_grad():
            kl_val = (p * torch.log(p / pi_ref)).sum()
            Js.append((p @ rewards - beta * kl_val).item())
            traj.append(theta.detach().clone().numpy())

        kl = (p * torch.log(p / pi_ref)).sum()

        if G is None:
            # 精确: 直接穷举求和, J₁ = Σ p(i)·r(i), 全程可微
            J1 = (p * rewards).sum()
            loss = -J1 + beta * kl
        else:
            # 采 G 个样本
            actions = torch.multinomial(p.detach(), G, replacement=True)  # [G]
            rs = rewards[actions]                                         # [G]
            log_probs = log_p[actions]                                    # [G]

            if use_baseline:
                advantage = rs - rs.mean()  # 组内均值 baseline
            else:
                advantage = rs

            # surrogate: -(1/G) Σ log π_θ(yᵢ) · advantage_i
            surrogate = -(log_probs * advantage.detach()).mean()
            loss = surrogate + beta * kl

        opt.zero_grad()
        loss.backward()
        opt.step()

    return np.array(traj), Js

# 跑不同配置
configs = [
    (1,    False, '$G=1$'),
    (4,    False, '$G=4$'),
    (4,    True,  '$G=4$ + baseline'),
    (16,   False, '$G=16$'),
    (None, False, 'exact (enumerate all)'),
]
results = {name: train(G, bl) for G, bl, name in configs}

# 可视化
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
colors_map = {'$G=1$': 'C0', '$G=4$': 'C1', '$G=4$ + baseline': 'C2',
              '$G=16$': 'C3', 'exact (enumerate all)': 'C4'}

# 自适应坐标轴范围: 覆盖所有轨迹 + θ*
all_pts = np.vstack([traj for traj, _ in results.values()] + [theta_star[None]])
pad = max((all_pts[:, 0].max() - all_pts[:, 0].min()) * 0.15, 1.0)
x_min = all_pts[:, 0].min() - pad
x_max = all_pts[:, 0].max() + pad
y_min = all_pts[:, 1].min() - pad
y_max = all_pts[:, 1].max() + pad

# 等高线背景 (与坐标轴同步)
t1 = np.linspace(x_min, x_max, 150)
t2 = np.linspace(y_min, y_max, 150)
T1, T2 = np.meshgrid(t1, t2)
Z = np.zeros_like(T1)
for i in range(150):
    for j in range(150):
        logits = np.array([T1[i,j], T2[i,j], 0.0])
        p = np.exp(logits - logits.max()); p /= p.sum()
        Z[i,j] = p @ rewards.numpy() - beta * (p * np.log(p / pi_ref.numpy())).sum()

# 上排: 每个配置的轨迹
for idx, (G, bl, name) in enumerate(configs):
    ax = axes[0][idx] if idx < 3 else axes[1][idx - 3]
    traj, Js = results[name]
    ax.contourf(T1, T2, Z, levels=30, cmap='RdYlGn', alpha=0.6)
    n = len(traj)
    cs = plt.cm.cool(np.linspace(0, 1, n))
    for i in range(n - 1):
        ax.plot(traj[i:i+2, 0], traj[i:i+2, 1], color=cs[i], lw=0.6, alpha=0.7)
    ax.plot(*traj[0], 's', color='blue', ms=8, zorder=10)
    ax.plot(*traj[-1], 'D', color='red', ms=8, zorder=10)
    ax.plot(*theta_star, '*', color='gold', ms=15, markeredgecolor='k', zorder=10)
    dist = np.linalg.norm(traj[-1] - theta_star)
    ax.set_title(f'{name}\nfinal dist to θ*: {dist:.2f}', fontsize=11)
    ax.set(xlabel=r'$\theta_1$', ylabel=r'$\theta_2$', xlim=(x_min, x_max), ylim=(y_min, y_max))

# 下排右: J 曲线对比
ax = axes[1][2]
w = 30
for G, bl, name in configs:
    _, Js = results[name]
    smoothed = np.convolve(Js, np.ones(w)/w, 'valid')
    ax.plot(range(w-1, len(Js)), smoothed, lw=2, label=name, color=colors_map[name])
ax.axhline(y=max(results['exact (enumerate all)'][1]), color='gold', ls='--', lw=1.5, label='$J^*$')
ax.set(xlabel='step', ylabel='$J(\\theta)$', title='$J(\\theta)$ convergence comparison')
ax.legend(fontsize=8); ax.grid(alpha=0.3)

plt.tight_layout()
# plt.savefig('/mnt/user-data/outputs/reinforce_multi_sample.png', dpi=150, bbox_inches='tight')
plt.show()

# 打印最终距离
print(f"{'config':<25} {'final θ':>20} {'dist to θ*':>12}")
for G, bl, name in configs:
    traj, _ = results[name]
    dist = np.linalg.norm(traj[-1] - theta_star)
    print(f"{name:<25} ({traj[-1,0]:+.2f}, {traj[-1,1]:+.2f})  {dist:>10.3f}")