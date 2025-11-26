#include <iostream>

class B;  // Tell compiler that B exists

class A {
private:
    int secret = 7;

    friend class B; // B is an intimate friend of A
    // friend B;    // Alternative
};

class B {
public:
    void reveal(A& a) {
        std::cout << a.secret << std::endl;
    }
};

int main() {
    A a;
    B b;
    b.reveal(a); // Outputs: 7
    return 0;
}
