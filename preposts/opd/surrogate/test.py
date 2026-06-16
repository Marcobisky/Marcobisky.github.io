import torch, numpy as np, matplotlib.pyplot as plt

# ============================================================
# Scenario: 1D walk (tiny MDP). Start at 0, take T steps, each +1/-1.
#   "token" = direction;  "prefix" = current position p.
#   Student (2 params): P(right|p) = sigmoid(theta1 + theta2*p)   [LINEAR in p]
#   Teacher: nonlinear mean-reverting, flat near center, strong at edges.
#            teacher logit(p) = clip(-0.5 * p*|p|, -8, 8)
#   -> linear student cannot match; off-policy vs on-policy fits differ.
# ============================================================
T = 6
PMAX = T
POSITIONS = np.arange(-PMAX, PMAX + 1)
pos_t = torch.arange(-PMAX, PMAX + 1).float()

def teacher_logit(p): return np.clip(-0.5 * p * np.abs(p), -8, 8)
TEACHER_PR = 1.0 / (1.0 + np.exp(-teacher_logit(POSITIONS)))
TEACHER_PR_T = torch.tensor(TEACHER_PR, dtype=torch.float32)

def stu_pr_np(t1, t2): return 1.0 / (1.0 + np.exp(-(t1 + t2 * POSITIONS)))
def kl_np(q, p):
    q = np.clip(q,1e-7,1-1e-7); p = np.clip(p,1e-7,1-1e-7)
    return q*np.log(q/p)+(1-q)*np.log((1-q)/(1-p))

def objective_np(t1, t2, on_policy):
    stu = stu_pr_np(t1,t2); kl = kl_np(TEACHER_PR, stu)
    trans = stu if on_policy else TEACHER_PR
    d = np.zeros(len(POSITIONS)); d[PMAX]=1.0; L=0.0
    for _ in range(T):
        L += d@kl
        nd = np.zeros_like(d)
        nd[1:] += d[:-1]*trans[:-1]; nd[:-1] += d[1:]*(1-trans[1:])
        d = nd
    return L

def objective_torch(theta, on_policy):
    stu = torch.clamp(torch.sigmoid(theta[0]+theta[1]*pos_t), 1e-7, 1-1e-7)
    q = TEACHER_PR_T
    kl = q*torch.log(q/stu)+(1-q)*torch.log((1-q)/(1-stu))
    trans = stu if on_policy else q
    d = torch.zeros(len(POSITIONS)); d[PMAX]=1.0; L=torch.zeros(())
    for _ in range(T):
        L = L + (d*kl).sum()
        right = torch.cat([torch.zeros(1), d[:-1]*trans[:-1]])
        left  = torch.cat([d[1:]*(1-trans[1:]), torch.zeros(1)])
        d = right + left
    return L

def train(on_policy, lr=0.05, n_steps=1500):
    theta = torch.zeros(2, requires_grad=True)
    opt = torch.optim.Adam([theta], lr=lr); traj=[]
    for _ in range(n_steps):
        traj.append(theta.detach().clone().numpy())
        loss = objective_torch(theta, on_policy)
        opt.zero_grad(); loss.backward(); opt.step()
    return np.array(traj), theta.detach().numpy()

traj_off, theta_off = train(False)
traj_on,  theta_on  = train(True)
print(f"off-policy optimum: ({theta_off[0]:.2f}, {theta_off[1]:.2f})")
print(f"on-policy  optimum: ({theta_on[0]:.2f}, {theta_on[1]:.2f})")

def visit_np(t1,t2,follow_student):
    pr = stu_pr_np(t1,t2) if follow_student else TEACHER_PR
    d = np.zeros(len(POSITIONS)); d[PMAX]=1.0; v=np.zeros(len(POSITIONS))
    for _ in range(T):
        v += d; nd=np.zeros_like(d)
        nd[1:]+=d[:-1]*pr[:-1]; nd[:-1]+=d[1:]*(1-pr[1:]); d=nd
    return v/v.sum()

fig, axes = plt.subplots(2,2,figsize=(15,13))
t1g=np.linspace(-1.2,1.2,120); t2g=np.linspace(-1.5,0.3,120)
T1,T2=np.meshgrid(t1g,t2g)
Zoff=np.vectorize(lambda a,b:objective_np(a,b,False))(T1,T2)
Zon =np.vectorize(lambda a,b:objective_np(a,b,True ))(T1,T2)

ax=axes[0,0]
ax.contourf(T1,T2,Zoff,levels=40,cmap='viridis_r',alpha=0.85)
ax.plot(traj_off[:,0],traj_off[:,1],'.-',color='cyan',ms=1.5,lw=0.7)
ax.plot(*theta_off,'D',color='red',ms=11,label=f'theta_off=({theta_off[0]:.2f},{theta_off[1]:.2f})')
ax.plot(*theta_on,'*',color='orange',ms=14,markeredgecolor='k')
ax.set(xlabel=r'$\theta_1$',ylabel=r'$\theta_2$',title='Off-policy objective  L_off = E[y~teacher][KL(q||pi)]')
ax.legend(fontsize=9)

ax=axes[0,1]
ax.contourf(T1,T2,Zon,levels=40,cmap='viridis_r',alpha=0.85)
ax.plot(traj_on[:,0],traj_on[:,1],'.-',color='cyan',ms=1.5,lw=0.7)
ax.plot(*theta_on,'*',color='orange',ms=16,markeredgecolor='k',label=f'theta_on=({theta_on[0]:.2f},{theta_on[1]:.2f})')
ax.plot(*theta_off,'D',color='red',ms=9)
ax.set(xlabel=r'$\theta_1$',ylabel=r'$\theta_2$',title='On-policy objective (OPD)  L_on = E[y~pi][KL(q||pi)]')
ax.legend(fontsize=9)

ax=axes[1,0]
fine=np.linspace(-PMAX,PMAX,200)
ax.plot(POSITIONS,TEACHER_PR,'ko-',ms=6,lw=2,label='teacher (nonlinear)')
ax.plot(fine,1/(1+np.exp(-(theta_off[0]+theta_off[1]*fine))),'--',color='red',lw=2,label='student @ theta_off')
ax.plot(fine,1/(1+np.exp(-(theta_on[0]+theta_on[1]*fine))),'--',color='orange',lw=2,label='student @ theta_on')
ax.axvspan(-PMAX,-2,alpha=0.08,color='blue'); ax.axvspan(2,PMAX,alpha=0.08,color='blue')
ax.set(xlabel='position p (prefix)',ylabel='P(right | p)',title='Policies: linear student vs nonlinear teacher\n(shaded = edges, student extrapolates)')
ax.legend(fontsize=9); ax.grid(alpha=0.3)

ax=axes[1,1]
vt=visit_np(*theta_off,False); voff=visit_np(*theta_off,True); von=visit_np(*theta_on,True)
ax.plot(POSITIONS,vt,'ko-',ms=5,lw=2,label='teacher visits (off-policy training prefixes)')
ax.plot(POSITIONS,voff,'s--',color='red',ms=5,label='theta_off visits at inference')
ax.plot(POSITIONS,von,'^--',color='orange',ms=5,label='theta_on visits at inference')
ax.set(xlabel='position p (prefix)',ylabel='visitation prob',title='Exposure bias: theta_off wanders to edges\nit was barely trained on')
ax.legend(fontsize=9); ax.grid(alpha=0.3)

Loff_inf=objective_np(*theta_off,True); Lon_inf=objective_np(*theta_on,True)
fig.suptitle(f'True loss on inference distribution:  theta_off={Loff_inf:.3f}  vs  theta_on={Lon_inf:.3f}   (off worse = exposure bias)',fontsize=13,y=1.0)
plt.tight_layout()
# plt.savefig('/mnt/user-data/outputs/walk_distillation.png',dpi=140,bbox_inches='tight')
plt.show()
print(f"true inference loss: theta_off={Loff_inf:.3f}, theta_on={Lon_inf:.3f}")