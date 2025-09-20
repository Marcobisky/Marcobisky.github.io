from train import TicTacToeAgent

def main():
    # Delete runs/ directory
    # shutil.rmtree('runs/', ignore_errors=True)

    agent = TicTacToeAgent()
        
    agent.train()
    agent.interactive_play()

if __name__ == "__main__":
    main()