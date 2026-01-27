class A:
    def forward(self, x):
        return x

class B(A):
    def forward(self, x):
        return 2 * x

def print_res(model: A, x: int):
    print(model.forward(x))

if __name__ == "__main__":
    m = B()
    print_res(m, 3)  # 6