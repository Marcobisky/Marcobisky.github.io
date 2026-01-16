class Car:
    # 常规初始化方法
    def __init__(self, color, model):
        self.color = color
        self.model = model
    
    # 两个可选的初始化方法
    @classmethod
    def init_from_dict(cls, init_dict): # cls 代表一个类名, 只是约定俗成叫 cls, 可以叫别的名字
        return cls(init_dict['color'], init_dict['model'])
    
    @classmethod
    def init_from_json(cls, json_str):
        import json
        init_dict = json.loads(json_str) # 将 json 字符串转换为字典
        return cls(init_dict['color'], init_dict['model'])
    
    # 一个sb降智方法
    @staticmethod
    def car_add_print_numbers(num1, num2):
        print(f"{num1 + num2} cars in total")
        
car1 = Car("red", "Toyota") # 使用常规初始化方法
car2 = Car.init_from_dict({'color': 'blue', 'model': 'Honda'}) # 使用字典初始化方法
car3 = Car.init_from_json('{"color": "green", "model": "Ford"}') # 使用 json 字符串初始化方法

Car.car_add_print_numbers(3, 5)  # Output: 8 cars in total
car1.car_add_print_numbers(10, 20)  # 用实例访问也行, Output: 30 cars in total