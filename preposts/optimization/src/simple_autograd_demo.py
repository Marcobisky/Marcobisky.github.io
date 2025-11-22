"""
简单模拟 PyTorch autograd 机制
关键: 每个操作返回的对象都记住了它的"父节点"
"""

class Tensor:
    def __init__(self, value, _children=()):
        self.value = value
        self._prev = set(_children)  # 记住我是从哪些节点计算来的
    
    def __mul__(self, other):
        out = Tensor(self.value * other.value, (self, other))
        print(f"  {self.value} * {other.value} = {out.value}, 记住了父节点")
        return out
    
    def __sub__(self, other):
        out = Tensor(self.value - other.value, (self, other))
        print(f"  {self.value} - {other.value} = {out.value}, 记住了父节点")
        return out

# 模拟训练过程
w = Tensor(2.0)
x = Tensor(3.0)
y_true = Tensor(5.0)

print("前向传播:")
y_pred = w * x          # y_pred 记住了 w 和 x
loss = y_pred - y_true  # loss 记住了 y_pred 和 y_true

print(f"\n虽然 loss 不知道模型结构,")
print(f"但 loss._prev 包含 y_pred: {y_pred in loss._prev}")
print(f"而 y_pred._prev 包含 w: {w in y_pred._prev}")
print(f"\n所以 loss 可以沿着这条链追溯到 w!")
