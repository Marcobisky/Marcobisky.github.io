import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
import matplotlib.pyplot as plt
from model import Position2Prob
from hyperparameters import *

# Initialize Model and Optimizer
model = Position2Prob()
optimizer = optim.Adam(model.parameters(), lr=lr)

# Training Loop (REINFORCE Algorithm)
for episode in range(num_episodes):
    # Start car at y=0, and a random x position on the highway
    state = np.array([np.random.uniform(x_min, x_max), y_min], dtype=np.float32)
    
    log_probs = []
    rewards = []
    
    # Run one complete episode
    while state[1] < y_max:
        # Convert state to tensor and get action probabilities
        state_tensor = torch.FloatTensor(state)
        probs = model(state_tensor)
        
        # Sample an action based on the probabilities
        m = Categorical(probs)
        action_idx = m.sample()
        
        # Save the log probability for the loss function calculation later
        log_probs.append(m.log_prob(action_idx))
        
        # Get velocity from the chosen action
        vx, vy = action_space[action_idx.item()]
        
        # Calculate environment dynamics (apply wind to x-velocity)
        dx = vx + wind(state) * wind_strength
        dy = vy
        
        # Update position and clip x to stay within highway boundaries
        next_state = np.array([
            np.clip(state[0] + dx * dt, x_min, x_max),
            state[1] + dy * dt
        ], dtype=np.float32)
        
        # Calculate and store reward
        r = reward(next_state)
        rewards.append(r)
        
        # Move to next step
        state = next_state
        
    # Calculate Discounted Returns (Gt)
    returns = []
    G = 0
    # Iterate backwards through the rewards to calculate cumulative return
    for r in reversed(rewards):
        G = r + gamma * G
        returns.insert(0, G)
    
    # Normalize returns (this makes training much more stable!)
    returns = torch.tensor(returns, dtype=torch.float32)
    returns = (returns - returns.mean()) / (returns.std() + 1e-9)
    
    # Calculate Policy Gradient Loss
    policy_loss = 0
    for log_prob, G in zip(log_probs, returns):
        policy_loss -= log_prob * G  # Negative because PyTorch minimizes loss, but we want to maximize Return
        
    # Backpropagation
    optimizer.zero_grad()
    policy_loss.backward()
    optimizer.step()
    
    # Print progress
    if (episode + 1) % 50 == 0:
        total_reward = sum(rewards)
        print(f"Episode {episode + 1:03d} | Total Reward: {total_reward:.2f} | Steps: {len(rewards)}")

print("Training finished!")

# save the model weights
torch.save(model.state_dict(), "windy_highway_model.pth")