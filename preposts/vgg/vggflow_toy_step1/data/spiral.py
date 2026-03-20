from __future__ import annotations

import math
import torch


def make_spiral(n: int, seed: int | None, device: str) -> torch.Tensor:
    """Generate n noisy 2D spiral points (2.5 turns, r from 0.15 to 1)."""
    gen = None
    if seed is not None:
        gen = torch.Generator(device="cpu")
        gen.manual_seed(seed)
    theta = torch.linspace(0, 2.5 * 2 * math.pi, n)
    r = 0.15 + theta / (2.5 * 2 * math.pi)
    pts = torch.stack([r * torch.cos(theta), r * torch.sin(theta)], dim=1)
    pts = pts + 0.05 * torch.randn((n, 2), generator=gen)
    return pts.to(device=device, dtype=torch.float32)


def sample_noise(n: int, seed: int | None, device: str) -> torch.Tensor:
    """Sample n points from N(0,I) in 2D."""
    gen = None
    if seed is not None:
        gen = torch.Generator(device="cpu")
        gen.manual_seed(seed)
    return torch.randn((n, 2), generator=gen, device=device, dtype=torch.float32)
