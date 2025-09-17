import random
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard.writer import SummaryWriter
from models import Net
from utils import *
from config import Config

class TicTacToeAgent:
    def __init__(self):
        self.config = Config()
        self.net = Net()
        self.target_net = Net()
        self.target_net.load_state_dict(self.net.state_dict())  # 将主网络参数复制到目标网络
        self.opt = optim.Adam(self.net.parameters(), lr=self.config.learning_rate)
        self.criterion = nn.MSELoss()
        self.buffer = []
        self.steps = 0
        self.writer = SummaryWriter('runs/tic_tac_toe_dqn')

    # Update the network once
    def train_step(self):
        if len(self.buffer) < self.config.batch_size: 
            return
        
        batch = random.sample(self.buffer, self.config.batch_size)
        s, a, r, s2, done = zip(*batch)
        s = torch.cat([to_tensor(x) for x in s])
        s2 = torch.cat([to_tensor(x) for x in s2])
        a = torch.tensor(a)
        r = torch.tensor(r, dtype=torch.float32)
        done = torch.tensor(done, dtype=torch.bool)

        q_values = self.net(s).gather(1, a.unsqueeze(1)).squeeze()  # 选择动作对应的Q值
        with torch.no_grad():
            q_next = self.target_net(s2).max(1)[0]  # 下一状态的最大Q值
            q_target = r + self.config.gamma * q_next * (~done)
        
        loss = self.criterion(q_values, q_target)
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()

        self.steps += 1
        if self.steps % self.config.update_target_every == 0:
            self.target_net.load_state_dict(self.net.state_dict())
        
        return loss.item()

    # Training by self-play
    def train(self):
        for episode in range(self.config.num_episodes):
            board = [0]*9
            idx_ai = 0 # To store AI's last action index
            reward = 0 # To store the reward
            player = 1  # AI is 1, opponent is -1
            result = None # Initialize the winner
            whos_turn = 0  # To track whose turn it is
            history = [] # To store (s, a, r, s2, done) tuples
            
            while result is None: # Game not over
                s = board.copy()  # Save current board state
                
                if whos_turn % 2 == 0:  # AI's turn
                    idx_ai = select_action(board, self.net, self.config.epsilon)
                    board[idx_ai] = player
                    result = check_win(board)
                    reward = result_to_reward(result)
    
                elif whos_turn % 2 == 1:  # Opponent's turn
                    idx_opp = env_move(board)
                    board[idx_opp] = -player
                    result = check_win(board)
                    reward = result_to_reward(result)
                
                whos_turn += 1
                
                if if_load_history(result, whos_turn):
                    done = True if result is not None else False
                    history.append((s, idx_ai, reward, board.copy(), done)) # Store this experience
                
            # Game ended, transmit all history to buffer
            for transition in history:
                self.buffer.append(transition)
            if len(self.buffer) > self.config.buffer_size: # Keep buffer size in limit
                self.buffer = self.buffer[-self.config.buffer_size:]
            loss = self.train_step()
            
            # Log to tensorboard every 100 episodes
            if episode % 100 == 0 and loss is not None:
                self.writer.add_scalar('Loss/Episode', loss, episode)

        print("Training completed.")
        self.writer.close()
                
    
    # Start play with updated network
    def interactive_play(self):
        print("欢迎与AI进行井字棋对战！")
        print("输入0-8选择位置，棋盘位置如下：")
        print("0|1|2")
        print("-----")
        print("3|4|5") 
        print("-----")
        print("6|7|8")
        print()
        
        board = [0] * 9
        human_player = -1  # 人类玩家是 -1 (O)
        ai_player = 1      # AI玩家是 1 (X)
        
        print("你是 O，AI是 X")
        print("当前棋盘：")
        print_board(board)
        
        while True:
            result = check_win(board)
            if result is not None:
                if result == human_player:
                    print("恭喜你获胜！")
                elif result == ai_player:
                    print("AI获胜！")
                else:
                    print("平局！")
                break
            
            # 人类玩家回合
            try:
                human_move = int(input("请输入你的位置选择 (0-8): "))
                if human_move < 0 or human_move > 8:
                    print("请输入0-8之间的数字")
                    continue
                if board[human_move] != 0:
                    print("该位置已被占用，请选择其他位置")
                    continue
                    
                board[human_move] = human_player
                print("你的选择：")
                print_board(board)
                
                # 检查人类是否获胜
                result = check_win(board)
                if result is not None:
                    continue  # 跳到循环开始处理游戏结束
                    
            except ValueError:
                print("请输入有效的数字")
                continue
            
            # AI回合
            ai_move = select_action(board, self.net, 0.0)  # epsilon=0，不使用随机探索
            board[ai_move] = ai_player
            print(f"AI选择位置 {ai_move}：")
            print_board(board)
        
        # 询问是否继续游戏
        play_again = input("是否再来一局？(y/n): ")
        if play_again.lower() == 'y':
            self.interactive_play()
        else:
            print("感谢游戏！")