from __future__ import annotations

import math
import torch
import torch.nn as nn


class TimeEmbedding(nn.Module):
    """Sinusoidal time embedding for t in [0, 1]."""

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        """Encode scalar t into 16-dim vector via sin/cos at multiple frequencies."""
        t = t.unsqueeze(1) if t.dim() == 1 else t
        half = 8
        freqs = torch.exp(-math.log(10000.0) * torch.arange(0, half, device=t.device, dtype=t.dtype) / 7)
        angles = t * freqs.unsqueeze(0)
        return torch.cat([torch.sin(angles), torch.cos(angles)], dim=1)
