# 一个示意的 LoRA 实现.
# 「示意」的原因是这里没有加载预训练权重, 也没有训练过程

import torch
import torch.nn as nn
import torch.nn.functional as F

# 一个带 LoRA 的线性层
class LinearWithLoRA(nn.Module):
    def __init__(self, in_dim, out_dim, r=4, scale=1.0):
        super().__init__()
        # 冻结基础权重
        self.base = nn.Linear(in_dim, out_dim)
        self.base.weight.requires_grad = False  # 冻结 base 权重

        # LoRA 的低秩矩阵 A 和 B
        self.A = nn.Parameter(torch.randn(r, in_dim) * 0.01)  # r×in_dim
        self.B = nn.Parameter(torch.randn(out_dim, r) * 0.01) # out_dim×r

        self.scale = scale

    def forward(self, x):
        # 原始线性输出
        out_base = self.base(x)
        # 计算 Delta W = B @ A
        delta_W = self.B @ self.A
        out_lora = F.linear(x, delta_W * self.scale)
        # 计算最终输出
        return out_base + out_lora

# 测试
model = LinearWithLoRA(128, 64, r=8)
input = torch.randn(16, 128)
out = model(input)
print(out.shape)
