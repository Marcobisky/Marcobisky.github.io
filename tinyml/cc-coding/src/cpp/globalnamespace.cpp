#include <iostream>

int value = 10;  // Global namespace value

namespace A {
    int value = 20;  // A::value

    void print() {
        std::cout << value << std::endl;      // Output 20
        std::cout << ::value << std::endl;    // Output 10
    }
}

int main() {
    A::print();
}
