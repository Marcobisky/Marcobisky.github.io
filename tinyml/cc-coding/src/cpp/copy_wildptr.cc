#include <iostream>
using namespace std;

int* g;

void store(int* p) {
    g = p;
}

int main() {
    {
        int x = 23;
        store(&x);
    }// x 生命周期结束
    // g 变成野指针
    cout << *g << endl;// 未定义
}