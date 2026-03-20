from __future__ import annotations

import torch


def sample_t(batch: int, device: str) -> torch.Tensor:
    """Sample batch of interpolation times uniformly in [0, 1]."""
    return torch.rand((batch, 1), device=device, dtype=torch.float32)


def flow_pair(x0: torch.Tensor, x1: torch.Tensor, t: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Return (x_t, target_v) for flow matching: x_t = (1-t)x0 + tx1, v = x1 - x0."""
    return (1 - t) * x0 + t * x1, x1 - x0
