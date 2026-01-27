#include <iostream>
using namespace std; // bad habits

class A {
public:
    int forward(int x) const {
        return x;
    }
};

class B : public A {
public:
    int forward(int x) const {
        return 2*x;
    }
};

void print_res(const A* model, int x) {
    cout << model->forward(x) << endl;
}

int main() {
    B* m = new B();
    print_res(m, 3); // 3
    delete m;
}
