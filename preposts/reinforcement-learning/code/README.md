# RL Tic-Tac-Toe

A reinforcement learning implementation of Tic-Tac-Toe using Deep Q-Learning (DQN) with PyTorch.

## Overview

This project implements an AI agent that learns to play Tic-Tac-Toe through self-play using deep reinforcement learning. The agent uses a neural network to approximate Q-values and employs techniques like experience replay and target networks.


## Installation

Create and activate the conda environment using the provided environment file:

```bash
conda env create -f environment.yml
conda activate rl_tic_tac_toe_env
```

## Usage

```bash
python main.py
```


## Project Structure

- `main.py` - Entry point of the application
- `train.py` - Training logic and TicTacToeAgent class
- `models.py` - Neural network architecture
- `utils.py` - Utility functions for game logic
- `config.py` - Training hyperparameters and configuration

