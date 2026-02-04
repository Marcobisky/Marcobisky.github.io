class A:
    def foo(self):
        print("A")
        
class B(A):
    def foo(self):
        print("B")
        super().foo()
        
class C(A):
    def foo(self):
        print("C")
        super().foo()
        
class D(B, C):  # 有顺序! B 比 C 更重要一点
    def foo(self):
        print("D")
        super().foo()

print(D.__mro__) 
# 输出: (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
D().foo()
# 输出: D B C A