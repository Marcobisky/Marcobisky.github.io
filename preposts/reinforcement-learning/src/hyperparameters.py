import numpy as np

x_min, x_max = 0, 1
y_min, y_max = 0, 1

wind = lambda p: np.cos(p[0]/np.pi*2)
wind_strength = 0.1
reward = lambda p: np.sin(p[0]/np.pi*2)

action_space = [(-1, 1), (0, 1), (1, 1)]


dt = 0.05           # Time step duration
gamma = 0.99        # Discount factor (values future rewards)
lr = 0.01           # Learning rate
num_episodes = 1000  # Total training episodes