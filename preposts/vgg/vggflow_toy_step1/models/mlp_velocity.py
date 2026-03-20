from __future__ import annotations

import torch
import torch.nn as nn

from models.time_embedding import TimeEmbedding


class MLPVelocity(nn.Module):
    """v_theta(x_t, t) for 2D flow matching."""

    def __init__(self) -> None:
        super().__init__()
        self.time_emb = TimeEmbedding()
        self.net = nn.Sequential(
            nn.Linear(18, 256), nn.SiLU(),
            nn.Linear(256, 256), nn.SiLU(),
            nn.Linear(256, 256), nn.SiLU(),
            nn.Linear(256, 2),
        )

    def forward(self, x_t: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        """Predict velocity v(x_t, t) given position and time."""
        emb = torch.cat([x_t, self.time_emb(t)], dim=1)
        return self.net(emb)
