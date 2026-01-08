def simple_decorator(func):
    def wrapper():
        print("函数执行前...")
        func()  # 调用原始函数
        print("函数执行后...")
    return wrapper

@simple_decorator
def say_hello():
    print("Hello!")

# 使用装饰器
say_hello() # Output:
            # 函数执行前...
            # Hello!
            # 函数执行后...