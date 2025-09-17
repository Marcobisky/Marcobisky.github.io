# 训练参数配置
class Config:
    # 模型参数
    buffer_size = 10000
    batch_size = 64
    gamma = 0.99
    epsilon = 0.1
    update_target_every = 1000
    learning_rate = 1e-3
    
    # 训练参数
    num_episodes = 50000