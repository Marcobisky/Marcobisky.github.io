#include <memory>
#include <iostream>

class B; // Let A know B

class A {
public:
    std::shared_ptr<B> bptr;
    ~A() { std::cout << "A destroyed\n"; }
};

class B {
public:
    std::shared_ptr<A> aptr;
    ~B() { std::cout << "B destroyed\n"; }
};

int main() {
    auto a = std::make_shared<A>(); // a1
    auto b = std::make_shared<B>(); // b1

    a->bptr = b; // b2
    b->aptr = a; // a2

    // No destroy messages!!! (Memory leak)
} // b1 a1 (not 0!)
