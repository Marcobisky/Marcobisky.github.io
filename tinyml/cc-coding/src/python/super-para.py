class A:
    def f(self):
        print("A.f")

class B(A):
    def f(self):
        print("B.f")
        super().f()         # Equivalent to call_super(B, self)
        
class C(B):
    def f(self):
        print("C.f")
        call_super(B, self) # C will skip B and call A.f()

def call_super(after, find_cls):
    super(after, find_cls).f()

c = C()
c.f()                       # Output: C.f A.f