# 1. 类可以赋值给变量
class Dog:
    def bark(self):
        return "Woof!"

Pet = Dog  # 类赋值给变量
my_dog = Pet()
print(my_dog.bark())  # 输出: Woof!

# 2. 类作为参数传递
def create_animal(cls, name):
    return cls(name)

class Cat:
    def __init__(self, name):
        self.name = name
    
    def meow(self):
        return f"{self.name} says Meow!"

cat = create_animal(Cat, "Whiskers")  # 传递类作为参数
print(cat.meow())  # 输出: Whiskers says Meow!