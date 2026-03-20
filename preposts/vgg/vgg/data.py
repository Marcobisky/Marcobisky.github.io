"""2D toy datasets for flow matching."""

from __future__ import annotations

import csv
from pathlib import Path

import torch
from torch.utils.data import Dataset


def _csv_path() -> Path:
    return Path(__file__).resolve().parent.parent / "src" / "smalldiffusion" / "datasets" / "DatasaurusDozen.tsv"


class DatasaurusDozen(Dataset):
    """2D point data from Datasaurus Dozen (e.g. dino, bullseye, h_lines)."""

    def __init__(self, dataset: str = "dino", csv_file: Path | str | None = None, enlarge_factor: int = 15, scale: float = 50, offset: float = 50):
        csv_file = csv_file or _csv_path()
        self.enlarge_factor = enlarge_factor
        self.points: list[torch.Tensor] = []
        with open(csv_file, newline="") as f:
            for name, *rest in csv.reader(f, delimiter="\t"):
                if name == dataset:
                    pt = torch.tensor(list(map(float, rest)))
                    self.points.append((pt - offset) / scale)

    def __len__(self) -> int:
        return len(self.points) * self.enlarge_factor

    def __getitem__(self, i: int) -> torch.Tensor:
        return self.points[i % len(self.points)]


class Swissroll(Dataset):
    """2D Swiss roll manifold."""

    def __init__(self, tmin: float, tmax: float, n: int, center: tuple[float, float] = (0, 0), scale: float = 1.0):
        t = tmin + torch.linspace(0, 1, n) * tmax
        c = torch.tensor(center).unsqueeze(0)
        self.vals = c + scale * torch.stack([t * torch.cos(t) / tmax, t * torch.sin(t) / tmax]).T

    def __len__(self) -> int:
        return len(self.vals)

    def __getitem__(self, i: int) -> torch.Tensor:
        return self.vals[i]

class SwissrollWithLabel(Dataset):
    """2D Swiss roll with 7 class labels, each class occupying a segment of the spiral."""

    NUM_CLASSES = 7

    def __init__(self, n_per_class: int = 300, noise: float = 0.02) -> None:
        tmin = torch.pi / 2
        tmax = 5 * torch.pi
        self.data: list[tuple[torch.Tensor, int]] = []

        for label in range(self.NUM_CLASSES):
            seg_start = tmin + (tmax - tmin) * label / self.NUM_CLASSES
            seg_end = tmin + (tmax - tmin) * (label + 1) / self.NUM_CLASSES
            t = torch.linspace(seg_start, seg_end, n_per_class)
            pts = torch.stack([t * torch.cos(t) / tmax, t * torch.sin(t) / tmax], dim=1)
            pts = pts + noise * torch.randn_like(pts)
            for i in range(n_per_class):
                self.data.append((pts[i], label))

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int]:
        return self.data[idx]
    

def sample_noise(n: int, device: str | torch.device = "cpu", seed: int | None = None) -> torch.Tensor:
    """Sample n points from N(0,I) in 2D."""
    gen = None
    if seed is not None:
        gen = torch.Generator(device="cpu")
        gen.manual_seed(seed)
    return torch.randn((n, 2), generator=gen, device=device, dtype=torch.float32)


