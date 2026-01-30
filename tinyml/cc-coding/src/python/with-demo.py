class MyContext:
    def __init__(self):
        print("I")
    def __enter__(self):
        print("A")
        return 1
    def __exit__(self, exc_type, exc_value, traceback):
        print("B")
        return 2

# 输出: I A Hi B
with MyContext():               # 如果你不需要用到 __enter__ 的返回值
    print("Hi")
    
print("-----")

# 输出: I A 3 1 4 B
with MyContext() as context:    # 如果你需要用到 __enter__ 的返回值
    print(3)
    print(context)
    print(4)

print("-----")

# 输出: I A 1 B
mycontext = MyContext()
with mycontext as context:      # 使用已有的 context 对象
    print(context)