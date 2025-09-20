# 训练参数配置
class Config:
    # 模型参数
    buffer_size = 10000
    batch_size = 64
    gamma = 0.99
    epsilon_start = 1.0
    epsilon_end = 0.01
    epsilon_decay = 0.995
    update_target_every = 100
    learning_rate = 1e-4
    
    # 训练参数
    num_episodes = 40000