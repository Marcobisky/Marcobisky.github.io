#include <memory>
#include <iostream>

class B; // Let A know B

class A {
public:
    std::weak_ptr<B> bptr;
    ~A() { std::cout << "A destroyed\n"; }
};

class B {
public:
    std::weak_ptr<A> aptr;
    ~B() { std::cout << "B destroyed\n"; }
};

int main() {
    auto a = std::make_shared<A>(); // a1
    auto b = std::make_shared<B>(); // b1

    a->bptr = b; // b1 still
    b->aptr = a; // a1 still

    // Destroy properly
} // a0 b0