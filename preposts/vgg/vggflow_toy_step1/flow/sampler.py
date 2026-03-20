from __future__ import annotations

from typing import Callable

import torch


@torch.no_grad()
def euler(x: torch.Tensor, t: torch.Tensor, dt: float, v_fn: Callable) -> torch.Tensor:
    """One Euler step: x_new = x + dt * v(x, t)."""
    return x + dt * v_fn(x, t)


@torch.no_grad()
def sample_trajectory(x0: torch.Tensor, v_fn: Callable, n_steps: int = 80) -> dict:
    """Integrate ODE from t=0 to 1 via Euler; return {xs, times}."""
    dt = 1.0 / n_steps
    times = torch.linspace(0, 1, n_steps + 1, device=x0.device, dtype=x0.dtype)
    xs = [x0.clone()]
    x = x0.clone()
    for i in range(n_steps):
        t = torch.full((x.size(0), 1), times[i].item(), device=x.device, dtype=x.dtype)
        x = euler(x, t, dt, v_fn)
        xs.append(x.clone())
    return {"xs": torch.stack(xs), "times": times}
