"""Flow matching: interpolation, loss, and ODE sampling."""

from __future__ import annotations

from typing import Callable

import torch


def sample_t(batch: int, device: str | torch.device) -> torch.Tensor:
    """Sample batch of times uniformly in [0, 1]."""
    return torch.rand((batch, 1), device=device, dtype=torch.float32)


def flow_pair(x0: torch.Tensor, x1: torch.Tensor, t: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Return (x_t, target_v): x_t = (1-t)x0 + tx1, v = x1 - x0."""
    return (1 - t) * x0 + t * x1, x1 - x0


def flow_matching_loss(pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    """MSE between predicted and target velocity."""
    return ((pred - target) ** 2).mean()


@torch.no_grad()
def sample_trajectory(x0: torch.Tensor, v_fn: Callable, n_steps: int = 80) -> dict:
    """Integrate ODE from t=0 to 1 via Euler; return {xs, times}."""
    dt = 1.0 / n_steps
    times = torch.linspace(0, 1, n_steps + 1, device=x0.device, dtype=x0.dtype)
    xs = [x0.clone()]
    x = x0.clone()
    for i in range(n_steps):
        t = torch.full((x.size(0), 1), times[i].item(), device=x.device, dtype=x.dtype)
        x = x + dt * v_fn(x, t)
        xs.append(x.clone())
    return {"xs": torch.stack(xs), "times": times}
