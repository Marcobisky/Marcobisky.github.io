#include <iostream>

namespace AppleSpace { namespace GoodApple {
    void print(const char* msg)
    {
        std::cout << "Goodapple " << msg << std::endl;
    }
}   namespace BadApple {
    void print(const char* msg)
    {
        std::cout << "Badapple " << msg << std::endl;
    }
} }

namespace OrangeSpace {
    void print(const char* msg)
    {
        std::cout << "Orange " << msg << std::endl;
    }
}

int main() {
    AppleSpace::GoodApple::print("Hello");
    AppleSpace::BadApple::print("Hello");
    OrangeSpace::print("Hello");
    return 0;
}