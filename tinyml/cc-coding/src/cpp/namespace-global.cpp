#include <iostream>

namespace A { int x = 1; }

namespace B {
namespace A { int x = 2; }

void f() {
    std::cout << A::x << std::endl;     // 表示当前命名空间下的 A
}
void g() {
    std::cout << ::A::x << std::endl;   // 表示全局命名空间下的 A
}
}

int main() {
    B::f();     // 输出: 2
    B::g();     // 输出: 1
}