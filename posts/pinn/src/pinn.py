import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from scipy.stats import qmc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# --- 1. Problem Setup ---
# 1D Heat Equation: u_t = ALPHA * u_xx
# Domain: x in [-1, 1], t in [0, 1]
# IC: u(x, 0) = -sin(pi * x)
# BC: u(-1, t) = 0, u(1, t) = 0
ALPHA = 1.0

MODEL_PATH = "pinn_heat.pth"
GIF_PATH = "heat_sine.gif"

# Function to compute exact solution for verification
def exact_solution(x, t):
    return -np.exp(-ALPHA * np.pi**2 * t) * np.sin(np.pi * x)


# --- 2. Data Generation ---
def generate_data(N_IC, N_BC, N_PDE):
    # a) Initial Condition Data
    x_ic = np.random.uniform(-1, 1, (N_IC, 1))
    t_ic = np.zeros((N_IC, 1))
    u_ic = -np.sin(np.pi * x_ic)

    # b) Boundary Condition Data
    x_bc_left = -np.ones((N_BC // 2, 1))
    t_bc_left = np.random.uniform(0, 1, (N_BC // 2, 1))
    u_bc_left = np.zeros((N_BC // 2, 1))

    x_bc_right = np.ones((N_BC // 2, 1))
    t_bc_right = np.random.uniform(0, 1, (N_BC // 2, 1))
    u_bc_right = np.zeros((N_BC // 2, 1))

    # c) PDE collocation points (Latin Hypercube Sampling)
    l_bounds = [-1.0, 0.0]
    u_bounds = [1.0, 1.0]

    sampler = qmc.LatinHypercube(d=2)
    sample = sampler.random(n=N_PDE)
    points_pde = qmc.scale(sample, l_bounds, u_bounds)

    x_pde = points_pde[:, 0:1]
    t_pde = points_pde[:, 1:2]

    def to_tensor(arr, requires_grad=False):
        return torch.tensor(
            arr, dtype=torch.float32, device=device, requires_grad=requires_grad
        )

    X_ic = to_tensor(x_ic)
    T_ic = to_tensor(t_ic)
    U_ic = to_tensor(u_ic)

    X_bc = to_tensor(np.vstack([x_bc_left, x_bc_right]))
    T_bc = to_tensor(np.vstack([t_bc_left, t_bc_right]))
    U_bc = to_tensor(np.vstack([u_bc_left, u_bc_right]))

    X_pde = to_tensor(x_pde, requires_grad=True)
    T_pde = to_tensor(t_pde, requires_grad=True)

    return X_ic, T_ic, U_ic, X_bc, T_bc, U_bc, X_pde, T_pde


# --- 3. Neural Network Design (PINN) ---
class PINN(nn.Module):
    def __init__(self, layers):
        super(PINN, self).__init__()
        self.linears = nn.ModuleList()
        for i in range(len(layers) - 1):
            layer = nn.Linear(layers[i], layers[i + 1])
            nn.init.xavier_normal_(layer.weight)
            nn.init.zeros_(layer.bias)
            self.linears.append(layer)

        self.activation = nn.Tanh()

    def forward(self, x, t):
        inputs = torch.cat([x, t], dim=1)
        for i in range(len(self.linears) - 1):
            inputs = self.activation(self.linears[i](inputs))
        output = self.linears[-1](inputs)
        return output


# --- 4. Training Function ---
def train(
    pinn,
    X_ic,
    T_ic,
    U_ic,
    X_bc,
    T_bc,
    U_bc,
    X_pde,
    T_pde,
    epochs=5000,
    lr=1e-3,
    w_pde=1.0,
    w_ic=10.0,
    w_bc=10.0,
):
    optimizer = optim.Adam(pinn.parameters(), lr=lr)
    losses = []

    pinn.train()
    for epoch in range(epochs):
        optimizer.zero_grad()

        # Initial condition loss
        u_ic_pred = pinn(X_ic, T_ic)
        loss_ic = torch.mean((u_ic_pred - U_ic) ** 2)

        # Boundary condition loss
        u_bc_pred = pinn(X_bc, T_bc)
        loss_bc = torch.mean((u_bc_pred - U_bc) ** 2)

        # PDE residual loss
        u_pde = pinn(X_pde, T_pde)

        u_t = torch.autograd.grad(
            u_pde, T_pde, torch.ones_like(u_pde), create_graph=True
        )[0]
        u_x = torch.autograd.grad(
            u_pde, X_pde, torch.ones_like(u_pde), create_graph=True
        )[0]
        u_xx = torch.autograd.grad(
            u_x, X_pde, torch.ones_like(u_x), create_graph=True
        )[0]

        residual_pde = u_t - ALPHA * u_xx
        loss_pde = torch.mean(residual_pde ** 2)

        total_loss = w_pde * loss_pde + w_ic * loss_ic + w_bc * loss_bc
        losses.append(total_loss.item())

        total_loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print(
                f"Epoch {epoch:5d}: Loss = {total_loss.item():.4e} "
                f"(IC: {loss_ic.item():.2e}, BC: {loss_bc.item():.2e}, PDE: {loss_pde.item():.2e})"
            )

    return losses


# --- 5. Save / Load ---
def save_checkpoint(model, loss_history, path=MODEL_PATH):
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "loss_history": loss_history,
        },
        path,
    )
    print(f"Model checkpoint saved to: {path}")


def load_checkpoint(model, path=MODEL_PATH):
    checkpoint = torch.load(path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    loss_history = checkpoint.get("loss_history", [])
    print(f"Loaded model checkpoint from: {path}")
    return loss_history


# --- 6. Evaluation ---
def predict_on_grid(model, nx=100, nt=100):
    x_test = np.linspace(-1, 1, nx)
    t_test = np.linspace(0, 1, nt)
    X_test, T_test = np.meshgrid(x_test, t_test)

    X_test_flat = torch.tensor(
        X_test.flatten()[:, None], dtype=torch.float32, device=device
    )
    T_test_flat = torch.tensor(
        T_test.flatten()[:, None], dtype=torch.float32, device=device
    )

    model.eval()
    with torch.no_grad():
        U_pred_flat = model(X_test_flat, T_test_flat)
        U_pred = U_pred_flat.cpu().numpy().reshape(nt, nx)

    U_exact = exact_solution(X_test, T_test)
    U_err = np.abs(U_exact - U_pred)

    return x_test, t_test, X_test, T_test, U_exact, U_pred, U_err


# --- 7. Static Plots ---
def plot_heatmaps(X_test, T_test, U_exact, U_pred, U_err):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    vmin = min(U_exact.min(), U_pred.min())
    vmax = max(U_exact.max(), U_pred.max())

    # Exact solution
    im0 = axes[0].pcolormesh(T_test, X_test, U_exact, cmap="seismic", shading="auto", vmin=vmin, vmax=vmax)
    axes[0].set_title("Exact Solution")
    axes[0].set_xlabel("Time t")
    axes[0].set_ylabel("Position x")
    fig.colorbar(im0, ax=axes[0])

    # PINN prediction
    im1 = axes[1].pcolormesh(T_test, X_test, U_pred, cmap="seismic", shading="auto", vmin=vmin, vmax=vmax)
    axes[1].set_title("PINN Prediction")
    axes[1].set_xlabel("Time t")
    axes[1].set_ylabel("Position x")
    fig.colorbar(im1, ax=axes[1])

    # Absolute error
    im2 = axes[2].pcolormesh(T_test, X_test, U_err, cmap="viridis", shading="auto")
    axes[2].set_title("Absolute Error")
    axes[2].set_xlabel("Time t")
    axes[2].set_ylabel("Position x")
    fig.colorbar(im2, ax=axes[2])

    plt.tight_layout()
    plt.show()


def plot_loss_history(loss_history):
    plt.figure(figsize=(8, 5))
    plt.plot(loss_history, linewidth=1.5)
    plt.xlabel("Epoch")
    plt.ylabel("Total Loss")
    plt.yscale("log")
    plt.title("Loss History")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# --- 8. Animated GIF ---
def save_animation_gif(x_test, t_test, U_exact, U_pred, U_err, gif_path=GIF_PATH):
    """
    这里做的是“时间切片动画”：
    每一帧固定一个 t，画出沿着 x 的三条/三类分布：
    1) exact temperature
    2) predicted temperature
    3) absolute error

    你要求温度纵坐标和 x 范围一致，所以温度子图设置 y in [-1, 1]。
    你原话里写 [-1,-1] 是错误区间，这里按 [-1,1] 实现。
    如果你更想看清 error，可以把 ax_err.set_ylim(0, U_err.max()*1.1)。
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax_temp, ax_err = axes

    line_exact, = ax_temp.plot([], [], lw=2, label="Exact", color="tab:blue")
    line_pred, = ax_temp.plot([], [], lw=2, label="Prediction", color="tab:orange")
    line_err, = ax_err.plot([], [], lw=2, label="Abs Error", color="tab:red")

    # Temperature subplot (exact vs prediction on same axes)
    ax_temp.set_title("Temperature Evolution (Exact vs PINN)")
    ax_temp.set_xlabel("Position x")
    ax_temp.set_ylabel("Temperature u(x,t)")
    ax_temp.set_xlim(-1, 1)
    ax_temp.set_ylim(-1, 1)
    ax_temp.grid(True, alpha=0.3)
    ax_temp.legend(loc="upper right")

    # Error subplot
    ax_err.set_title("Absolute Error Evolution")
    ax_err.set_xlabel("Position x")
    ax_err.set_ylabel("|u_exact - u_pred|")
    ax_err.set_xlim(-1, 1)
    # Automatically adjust y-limits based on error range
    ax_err.set_ylim(0, U_err.max() * 1.1)
    ax_err.grid(True, alpha=0.3)
    ax_err.legend(loc="upper right")

    time_text = fig.suptitle("", fontsize=14)

    def init():
        line_exact.set_data([], [])
        line_pred.set_data([], [])
        line_err.set_data([], [])
        time_text.set_text("")
        return line_exact, line_pred, line_err, time_text

    def update(frame):
        y_exact = U_exact[frame, :]
        y_pred = U_pred[frame, :]
        y_err = U_err[frame, :]

        line_exact.set_data(x_test, y_exact)
        line_pred.set_data(x_test, y_pred)
        line_err.set_data(x_test, y_err)

        time_text.set_text(f"Time evolution at t = {t_test[frame]:.3f}")
        return line_exact, line_pred, line_err, time_text

    anim = FuncAnimation(
        fig,
        update,
        frames=len(t_test),
        init_func=init,
        blit=True,
        interval=80,
        repeat=True,
    )

    anim.save(gif_path, writer=PillowWriter(fps=12))
    plt.close(fig)
    print(f"Animated GIF saved to: {gif_path}")


# --- Main Execution ---
if __name__ == "__main__":
    # Settings
    N_IC_points = 50
    N_BC_points = 4
    N_PDE_points = 5000
    pinn_layers = [2, 20, 20, 20, 20, 1]

    # Reproducibility
    torch.manual_seed(42)
    np.random.seed(42)

    # 1. Generate Data
    print("Generating data...")
    X_ic, T_ic, U_ic, X_bc, T_bc, U_bc, X_pde, T_pde = generate_data(
        N_IC_points, N_BC_points, N_PDE_points
    )

    # 2. Design Network
    print("Designing network...")
    pinn_model = PINN(pinn_layers).to(device)

    # 3. Train or Load
    if os.path.exists(MODEL_PATH):
        print(f"Found existing model file: {MODEL_PATH}")
        loss_history = load_checkpoint(pinn_model, MODEL_PATH)
    else:
        print("No existing model file found. Starting training...")
        loss_history = train(
            pinn_model,
            X_ic,
            T_ic,
            U_ic,
            X_bc,
            T_bc,
            U_bc,
            X_pde,
            T_pde,
            epochs=500,
            lr=1e-3,
            w_ic=100.0,
            w_bc=100.0,
        )
        save_checkpoint(pinn_model, loss_history, MODEL_PATH)

    # 4. Evaluation
    print("Evaluating...")
    x_test, t_test, X_test, T_test, U_exact, U_pred, U_err = predict_on_grid(
        pinn_model, nx=100, nt=100
    )

    # 5. Static plots: (a)
    plot_heatmaps(X_test, T_test, U_exact, U_pred, U_err)

    # 6. Loss history: (b)
    plot_loss_history(loss_history)

    # 7. Animated GIF: (c)
    save_animation_gif(x_test, t_test, U_exact, U_pred, U_err, GIF_PATH)