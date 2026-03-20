from __future__ import annotations

import torch


def flow_matching_loss(pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    """MSE between predicted and target velocity."""
    return ((pred - target) ** 2).mean()
