import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
import matplotlib.pyplot as plt
from model import Position2Prob
from hyperparameters import *


# load the trained model weights
model = Position2Prob()
model.load_state_dict(torch.load("windy_highway_model.pth"))
model.eval()  # Set the model to evaluation mode

# Use the model to plot a trajectory after training
# Generate some random starting positions at y=0
num_trajectories = 20
trajectories = []
for _ in range(num_trajectories):
    state = np.array([np.random.uniform(x_min, x_max), y_min], dtype=np.float32)
    trajectory = [state.copy()]
    
    while state[1] < y_max:
        state_tensor = torch.FloatTensor(state)
        with torch.no_grad():
            probs = model(state_tensor)
        
        action_idx = torch.argmax(probs).item()  # Choose the action with highest probability
        vx, vy = action_space[action_idx]
        
        dx = vx + wind(state) * wind_strength
        dy = vy
        
        state[0] = np.clip(state[0] + dx * dt, x_min, x_max)
        state[1] += dy * dt
        
        trajectory.append(state.copy())
    
    trajectories.append(np.array(trajectory))

# Plot the trajectories
plt.figure(figsize=(8, 6))
for i, traj in enumerate(trajectories):
    plt.plot(traj[:, 0], traj[:, 1], label=f'Trajectory {i+1}')
plt.title('Car Trajectories on Windy Highway')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.legend()
plt.grid()
plt.show()