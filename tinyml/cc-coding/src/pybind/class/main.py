from ml_ops import Model, LinearModel

# 使用基类
model = Model()
print(model.forward(2.0))               # 2.0

# 使用派生类
linearModel = LinearModel(weight=3.0)
print(linearModel.forward(2.0))         # 6.0

# 验证继承关系
print(isinstance(linearModel, Model))   # True

# 访问 C++ 成员变量
print(linearModel.weight)               # 3.0
linearModel.weight = 5.0
print(linearModel.forward(2.0))         # 10.0