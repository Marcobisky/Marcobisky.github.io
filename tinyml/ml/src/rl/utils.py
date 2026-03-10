import random
from collections import deque
import torch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# Tic-Tac-Toe helpers
# We always encode from the current player's perspective:
# current player = 1
# opponent = -1
# empty = 0
# =========================
WIN_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def check_winner(board, player):
    """Return True if 'player' has a winning line."""
    for a, b, c in WIN_LINES:
        if board[a] == board[b] == board[c] == player:
            return True
    return False


def is_full(board):
    return all(x != 0 for x in board)


def legal_actions(board):
    return [i for i, x in enumerate(board) if x == 0]


def apply_action(board, action, player):
    """Return a new board after player places at action."""
    new_board = board[:]
    new_board[action] = player
    return new_board


def to_current_player_view(board):
    """
    Convert board to the current player's perspective.
    In this simplified generator, after opponent moves,
    we flip signs so the next state is again from the
    next current player's perspective.
    """
    return board[:]


def masked_argmax(q_values, board):
    """Pick the best legal action from q_values."""
    legal = legal_actions(board)
    if not legal:
        return None
    best_action = legal[0]
    best_value = q_values[best_action].item()
    for a in legal[1:]:
        if q_values[a].item() > best_value:
            best_value = q_values[a].item()
            best_action = a
    return best_action


# =========================
# Replay Buffer
# =========================
class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, s, a, r, s2, done):
        self.buffer.append((s, a, r, s2, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        s, a, r, s2, done = zip(*batch)
        return (
            torch.tensor(s, dtype=torch.float32, device=DEVICE),
            torch.tensor(a, dtype=torch.long, device=DEVICE),
            torch.tensor(r, dtype=torch.float32, device=DEVICE),
            torch.tensor(s2, dtype=torch.float32, device=DEVICE),
            torch.tensor(done, dtype=torch.float32, device=DEVICE),
        )

    def __len__(self):
        return len(self.buffer)
