import random
import numpy as np
import torch

# Return the winner, 0 for tie, None for ongoing
def check_win(board):
    winning_pattern = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in winning_pattern:
        if board[a]==board[b]==board[c]!=0:
            return board[a] # Return the winner (1 or -1)
    if 0 not in board:
        return 0  # Tie
    return None  # Not finished

# Convert board state to tensor
def to_tensor(board):
    return torch.tensor(board, dtype=torch.float32).unsqueeze(0)

# Return the index of the action to take
def select_action(board, net, epsilon):
    if random.random() < epsilon: # Small chance to explore
        return random.choice([i for i,x in enumerate(board) if x==0])
    # Choose the action with the highest Q-value among valid moves
    with torch.no_grad():
        q = net(to_tensor(board)).numpy()[0]
    q_valid = [q[i] if board[i]==0 else -1e9 for i in range(9)]
    return int(np.argmax(q_valid))

# Opponent: random move, return the index
def env_move(board):
    opp_moves = [i for i,x in enumerate(board) if x==0]
    env_idx = random.choice(opp_moves)
    return env_idx

# Result to reward
def result_to_reward(result):
    if result == 0: # Tie
        return 0
    elif result == 1: # AI Win
        return 1
    elif result == -1: # Opponent Win
        return -1
    else: # Ongoing
        return 0 
    
# Load history
def if_load_history(result, whos_turn):
    if whos_turn % 2 == 1: # Opponent just played
        return True
    elif result == 1: # AI just won
        return True
    else: # Tie or ongoing
        return False
    
# Print the board
def print_board(board):
    symbols = {1: 'X', -1: 'O', 0: ' '}
    for i in range(3):
        row = [symbols[board[j]] for j in range(i*3, (i+1)*3)]
        print('|'.join(row))
        if i < 2:
            print('-----')
    print()