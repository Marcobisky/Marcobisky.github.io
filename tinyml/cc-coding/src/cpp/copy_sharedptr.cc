#include <iostream>
using namespace std;

shared_ptr<int> g_shared;

void store(shared_ptr<int> p) {
    g_shared = p;   // 复制
}

int main() {
    {
        auto x = make_shared<int>(23);
        store(x);
    }// main 里的 x 消失, 但对象还活着
    // g_shared 仍然有效
    cout << *g_shared << endl; // 23
}