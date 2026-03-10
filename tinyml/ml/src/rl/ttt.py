import random
from collections import deque

import torch
import torch.nn as nn
import torch.nn.functional as F
from utils import *

# =========================
# Hyperparameters
# =========================
GAMMA = 0.99
LR = 1e-4
BATCH_SIZE = 64
BUFFER_SIZE = 5000
TARGET_UPDATE_FREQ = 100
NUM_EPISODES = 3000


# =========================
# Q Network
# =========================
class QNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(9, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 9)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


# =========================
# Data generation
# One transition = current player moves once,
# then opponent randomly moves once (if game not over).
# Reward is from the current player's perspective.
# =========================
def generate_training_data(net, epsilon=0.2):
    """
    Generate ONE transition: (s, a, r, s2, done)

    State s: current player's perspective
    Action a: chosen by epsilon-greedy on net
    Reward r:
        +1 if current player wins immediately
        -1 if opponent wins after its random response
         0 otherwise / draw
    s2: next state, again converted to the next current player's perspective
    done: whether the game has ended
    """
    board = [0] * 9

    # Randomize a partial position a bit so data is not always from empty board.
    # We generate a valid random prefix by alternating random moves.
    # Current player is always encoded as 1 in the returned state.
    num_random_moves = random.randint(0, 4)
    current_player = 1

    for _ in range(num_random_moves):
        actions = legal_actions(board)
        if not actions:
            break
        a = random.choice(actions)
        board[a] = current_player

        if check_winner(board, current_player):
            # restart if random prefix already ends the game
            board = [0] * 9
            current_player = 1
            break

        current_player *= -1

    # Re-encode so that current player is always +1
    if current_player == -1:
        board = [-x for x in board]

    s = board[:]

    # Choose action for current player using epsilon-greedy
    legal = legal_actions(s)
    if not legal:
        return s, 0, 0.0, s, 1.0  # degenerate fallback

    if random.random() < epsilon:
        a = random.choice(legal)
    else:
        with torch.no_grad():
            q_values = net(torch.tensor([s], dtype=torch.float32, device=DEVICE))[0]
        a = masked_argmax(q_values, s)

    # Current player moves
    after_my_move = apply_action(s, a, 1)

    # If I win immediately
    if check_winner(after_my_move, 1):
        r = 1.0
        done = 1.0
        s2 = after_my_move[:]  # terminal, value will be masked by done
        return s, a, r, s2, done

    # If board full -> draw
    if is_full(after_my_move):
        r = 0.0
        done = 1.0
        s2 = after_my_move[:]
        return s, a, r, s2, done

    # Opponent responds randomly
    opp_legal = legal_actions(after_my_move)
    opp_action = random.choice(opp_legal)
    after_opp_move = apply_action(after_my_move, opp_action, -1)

    # If opponent wins, from my perspective reward is -1
    if check_winner(after_opp_move, -1):
        r = -1.0
        done = 1.0
        s2 = [-x for x in after_opp_move]  # flip to next current player's view
        return s, a, r, s2, done

    # If board full after opponent move -> draw
    if is_full(after_opp_move):
        r = 0.0
        done = 1.0
        s2 = [-x for x in after_opp_move]
        return s, a, r, s2, done

    # Otherwise non-terminal, next player's perspective
    r = 0.0
    done = 0.0
    s2 = [-x for x in after_opp_move]
    return s, a, r, s2, done


# =========================
# Training
# =========================
def train():
    net = QNet().to(DEVICE)
    target_net = QNet().to(DEVICE)
    target_net.load_state_dict(net.state_dict())
    target_net.eval()

    optimizer = torch.optim.Adam(net.parameters(), lr=LR)
    replay_buffer = ReplayBuffer(BUFFER_SIZE)

    global_step = 0

    for episode in range(NUM_EPISODES):
        # epsilon slowly decreases
        epsilon = max(0.05, 0.3 - 0.25 * (episode / NUM_EPISODES))

        # Generate one transition and store it
        s, a, r, s2, done = generate_training_data(net, epsilon)
        replay_buffer.push(s, a, r, s2, done)

        # Start training only when buffer has enough samples
        if len(replay_buffer) < BATCH_SIZE:
            continue

        states, actions, rewards, next_states, dones = replay_buffer.sample(BATCH_SIZE)

        # Current Q(s, a)
        q_all = net(states)  # [B, 9]
        q_pred = q_all.gather(1, actions.unsqueeze(1)).squeeze(1)  # [B]

        # Target: r + gamma * max_a' Q_target(s2, a') * (1 - done)
        with torch.no_grad():
            q_next_all = target_net(next_states)  # [B, 9]

            # Mask illegal actions in next_states
            mask = (next_states == 0)  # legal if cell == 0
            q_next_all = q_next_all.masked_fill(~mask, -1e9)

            q_next = q_next_all.max(dim=1)[0]  # [B]
            q_target = rewards + GAMMA * q_next * (1.0 - dones)

        loss = F.mse_loss(q_pred, q_target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        global_step += 1

        # Periodically update target network
        if global_step % TARGET_UPDATE_FREQ == 0:
            target_net.load_state_dict(net.state_dict())

        if (episode + 1) % 200 == 0:
            print(
                f"Episode {episode + 1:4d} | "
                f"epsilon={epsilon:.3f} | "
                f"buffer={len(replay_buffer):4d} | "
                f"loss={loss.item():.4f}"
            )

    return net, target_net


if __name__ == "__main__":
    net, target_net = train()