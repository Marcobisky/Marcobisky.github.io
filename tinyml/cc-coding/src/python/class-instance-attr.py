class Car:
    # Class attributes
    wheels = 4
    count = 0
    
    def __init__(self, color, model):
        # Instance attributes
        self.color = color
        self.model = model
        Car.count += 1 # 每创建这样的类时, 计数加 1
        
print(Car.wheels)  # Accessing class attribute
# print(Car.color) # Cannot access instance attribute without creating instances

car1 = Car("red", "Toyota")
car2 = Car("blue", "Honda")
print(car1.color)

print(Car.count)  # Output: 2