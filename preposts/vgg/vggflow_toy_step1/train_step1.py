from __future__ import annotations

import torch
from torch.utils.data import DataLoader, TensorDataset

from data.spiral import make_spiral, sample_noise
from flow.interpolation import flow_pair, sample_t
from flow.losses import flow_matching_loss
from flow.sampler import sample_trajectory
from models.mlp_velocity import MLPVelocity
from viz import show_flow_animation, show_spiral

DEVICE = "cpu"
SEED = 42


def train() -> tuple[torch.nn.Module, list[float]]:
    """Train flow matching on spiral data; return model and loss history."""
    torch.manual_seed(SEED)
    device = torch.device(DEVICE)

    x1 = make_spiral(12000, SEED, DEVICE)
    model = MLPVelocity().to(device)
    loader = DataLoader(TensorDataset(x1), batch_size=512, shuffle=True, drop_last=True)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=1000, eta_min=1e-5)
    loss_hist = []

    n_batches = len(loader)
    for epoch in range(1000):
        epoch_loss = 0.0
        for (x1_b,) in loader:
            x0 = sample_noise(x1_b.size(0), None, DEVICE)
            t = sample_t(x1_b.size(0), DEVICE)
            x_t, target_v = flow_pair(x0, x1_b, t)
            pred_v = model(x_t, t)
            loss = flow_matching_loss(pred_v, target_v)
            opt.zero_grad()
            loss.backward()
            opt.step()
            epoch_loss += loss.item()
        loss_hist.append(epoch_loss / n_batches)
        sched.step()
        if (epoch + 1) % 100 == 0:
            print(f"epoch={epoch + 1:04d} loss={loss_hist[-1]:.6f}")

    return model, loss_hist


def main() -> None:
    """Train, show spiral, show flow animation."""
    model, _ = train()
    device = torch.device(DEVICE)
    target = make_spiral(1000, SEED + 1, DEVICE)
    gaussian = sample_noise(1000, SEED + 2, DEVICE)
    traj = sample_trajectory(gaussian, lambda x, t: model(x, t), n_steps=80)

    show_spiral(target)
    show_flow_animation(lambda x, t: model(x, t), traj, device)


if __name__ == "__main__":
    main()
