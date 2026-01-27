#include <iostream>

class Print {
public:
    void show(int i) {
        std::cout << "Integer: " << i << std::endl;
    }

    void show(double d) {
        std::cout << "Double: " << d << std::endl;
    }

    void show(const std::string& s) {
        std::cout << "String: " << s << std::endl;
    }
};

int main() {
    Print p;
    p.show(5);          // 输出: Integer: 5
    p.show(3.14);       // 输出: Double: 3.14
    p.show("Hello");    // 输出: String: Hello

    return 0;
}