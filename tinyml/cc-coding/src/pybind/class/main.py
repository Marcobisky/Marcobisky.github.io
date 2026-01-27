from ml_ops import Model, LinearModel

# 使用基类
m = Model()
print(m.forward(2.0))   # 输出 2.0

# 使用派生类
lm = LinearModel(weight=3.0)
print(lm.forward(2.0))  # 输出 6.0

# 验证继承关系
print(isinstance(lm, Model))  # True

# 访问 C++ 成员变量
print(lm.weight)
lm.weight = 5.0
print(lm.forward(2.0))  # 输出 10.0
