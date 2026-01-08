# 1. 赋值给变量
def greet(name):
    return f"Hello, {name}!"

my_function = greet  # 函数赋值给变量
print(my_function("Alice"))  # 输出: Hello, Alice!

# 2. 作为参数传递
def shout(func, name):
    result = func(name)
    return result.upper()

print(shout(greet, "Bob"))  # 输出: HELLO, BOB!

# 3. 作为返回值, 这里也可以用装饰器!
def simple_decorator(func):
    def wrapper():
        print("函数执行前...")
        func()  # 调用原始函数
        print("函数执行后...")
    return wrapper

def say_hello():
    print("Hello!")

simple_decorator(say_hello)() # 输出:
                              # 函数执行前...
                              # Hello!
                              # 函数执行后...

# 4. 存储在数据结构中
operations = {
    'add': lambda x, y: x + y,
    'subtract': lambda x, y: x - y,
    'multiply': lambda x, y: x * y
}

print(operations['add'](10, 5))      # 输出: 15
print(operations['multiply'](3, 4))  # 输出: 12
