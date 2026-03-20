from __future__ import annotations

from typing import Callable

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import torch


def show_spiral(pts: torch.Tensor) -> None:
    """Static plot of target spiral."""
    arr = pts.detach().cpu().numpy()
    plt.figure(figsize=(5, 5))
    plt.scatter(arr[:, 0], arr[:, 1], alpha=0.65, s=8)
    plt.title("Target spiral")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


def show_flow_animation(
    v_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
    traj: dict,
    device: torch.device,
) -> None:
    """Animate: time-varying vector field (unit arrows, color=mag) + points moving along ODE."""
    xs = traj["xs"][:, :300].detach().cpu().numpy()
    times = traj["times"].detach().cpu().numpy()
    g = torch.linspace(-2.5, 2.5, 15, device=device)
    gx, gy = torch.meshgrid(g, g, indexing="xy")
    grid = torch.stack([gx.reshape(-1), gy.reshape(-1)], dim=1)
    xy = grid.cpu().numpy()

    fig, ax = plt.subplots(figsize=(6, 6))
    t0 = torch.zeros((grid.size(0), 1), device=device)
    v0 = v_fn(grid, t0).detach().cpu().numpy()
    mag0 = np.sqrt((v0**2).sum(axis=1))
    mag0_safe = np.maximum(mag0, 1e-8)
    u0, v0_n = v0[:, 0] / mag0_safe, v0[:, 1] / mag0_safe
    qv = ax.quiver(xy[:, 0], xy[:, 1], u0, v0_n, mag0, cmap="viridis", scale=15, scale_units="xy", alpha=0.8)
    plt.colorbar(qv, ax=ax, label="|v|")
    scat = ax.scatter(xs[0, :, 0], xs[0, :, 1], s=12, alpha=0.8, c="red")
    title = ax.set_title("t=0.00")
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect("equal")

    def update(i):
        t_val = float(times[i])
        t = torch.full((grid.size(0), 1), t_val, device=device, dtype=grid.dtype)
        v = v_fn(grid, t).detach().cpu().numpy()
        mag = np.sqrt((v**2).sum(axis=1))
        mag_safe = np.maximum(mag, 1e-8)
        u, v_n = v[:, 0] / mag_safe, v[:, 1] / mag_safe
        qv.set_UVC(u, v_n, mag)
        scat.set_offsets(xs[i, :, :2])
        title.set_text(f"t={t_val:.2f}")
        return scat, qv, title

    ani = animation.FuncAnimation(fig, update, frames=xs.shape[0], interval=50, blit=False)
    plt.tight_layout()
    plt.show()
