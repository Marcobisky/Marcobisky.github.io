from train import TicTacToeAgent

def main():
    agent = TicTacToeAgent()
        
    agent.train()
    agent.interactive_play()

if __name__ == "__main__":
    main()